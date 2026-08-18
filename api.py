import os
import uuid
import base64
import zipfile
import io
from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from fpdf import FPDF

from core.graph import build_compliance_graph
from core.tools import tool_llm
from core.auth import get_db, User, verify_password, get_password_hash, create_access_token, decode_access_token, supabase, get_current_user_from_token

app = FastAPI(title="Guardian AI Backend")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_compliance_graph()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# --- Authentication Dependencies ---
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_current_user_from_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user

# --- Pydantic Models ---
class UserCreate(BaseModel):
    email: str
    password: str

class AuditRequest(BaseModel):
    red_team_mode: bool = False
    federated_mode: bool = False
    jurisdiction: str = "Global (PCI-DSS)"
    image_base64: Optional[str] = None
    audio_base64: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    thread_id: str

# --- Auth Endpoints ---
@app.post("/api/register")
def register(user: UserCreate):
    try:
        res = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        if res and res.user:
            return {
                "access_token": res.session.access_token,
                "token_type": "bearer",
                "is_pro": res.user.user_metadata.get("is_pro", False)
            }
        raise HTTPException(status_code=400, detail="Registration failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": form_data.username,
            "password": form_data.password
        })
        if res and res.user:
            return {
                "access_token": res.session.access_token,
                "token_type": "bearer",
                "is_pro": res.user.user_metadata.get("is_pro", False)
            }
        raise HTTPException(status_code=400, detail="Login failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

# --- Core Logic Endpoints ---
upload_cache = {}

@app.post("/api/upload_codebase")
async def upload_codebase(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    content = await file.read()
    extracted_text = ""
    
    if file.filename.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            for filename in z.namelist():
                if filename.endswith((".py", ".js", ".ts", ".tsx", ".md", ".txt", ".json")):
                    try:
                        extracted_text += f"\n--- {filename} ---\n"
                        extracted_text += z.read(filename).decode('utf-8')[:1000]
                    except Exception:
                        pass
    else:
        extracted_text = content.decode('utf-8')[:5000]

    upload_cache[current_user.email] = extracted_text[:10000]
    return {"status": "success", "message": "Codebase uploaded and analyzed."}


@app.post("/api/audit")
def run_audit(req: AuditRequest, current_user: User = Depends(get_current_user)):
    thread_id = f"{current_user.id}_{uuid.uuid4().hex[:8]}"
    config = {"configurable": {"thread_id": thread_id}}
    
    img_bytes = base64.b64decode(req.image_base64) if req.image_base64 else None
    aud_bytes = base64.b64decode(req.audio_base64) if req.audio_base64 else None

    code_context = upload_cache.get(current_user.email, None)

    inputs = {
        "findings": [],
        "risk_level": "UNKNOWN",
        "scout_retries": 0,
        "red_team_mode": req.red_team_mode,
        "federated_mode": req.federated_mode,
        "uploaded_image_bytes": img_bytes,
        "audio_bytes": aud_bytes,
        "jurisdiction": req.jurisdiction,
        "user_codebase_context": code_context
    }
    
    graph.invoke(inputs, config=config)
    snapshot = graph.get_state(config)
    
    state_values = dict(snapshot.values) if snapshot.values else {}
    if "uploaded_image_bytes" in state_values:
        del state_values["uploaded_image_bytes"]
    if "audio_bytes" in state_values:
        del state_values["audio_bytes"]
        
    return {
        "thread_id": thread_id,
        "state": state_values,
        "is_paused": bool(snapshot.next)
    }

@app.post("/api/deploy")
def deploy_patch(thread_id: str, current_user: User = Depends(get_current_user)):
    config = {"configurable": {"thread_id": thread_id}}
    graph.invoke(None, config)
    return {"status": "deployed"}

@app.post("/api/chat")
def chat(req: ChatRequest, current_user: User = Depends(get_current_user)):
    config = {"configurable": {"thread_id": req.thread_id}}
    snapshot = graph.get_state(config)
    
    if not snapshot or not snapshot.values:
        return {"response": "Session not found or telemetry unavailable."}
        
    state_context = str(snapshot.values)
    
    try:
        if tool_llm:
            resp = tool_llm.invoke(f"System Context: {state_context[:2000]}\nUser: {req.message}\nAnswer as Guardian AI.").content
        else:
            resp = "I am Guardian AI. LLM backend is offline."
    except Exception as e:
        resp = f"Error communicating with LLM: {str(e)}"
        
    return {"response": resp}

# --- PDF Export ---
@app.get("/api/export/{thread_id}")
def export_pdf(thread_id: str, current_user: User = Depends(get_current_user)):
    config = {"configurable": {"thread_id": thread_id}}
    snapshot = graph.get_state(config)
    
    if not snapshot or not snapshot.values:
        raise HTTPException(status_code=404, detail="Audit not found")
        
    state = snapshot.values
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    pdf.cell(200, 10, txt="Guardian AI - Compliance Audit Report", align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Jurisdiction: {state.get('jurisdiction', 'N/A')}")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Risk Level: {state.get('risk_level', 'N/A')}")
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Findings:")
    pdf.ln(10)
    for f in state.get("findings", []):
        clean_text = f.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=f"- {clean_text}")
        
    pdf_output_path = f"report_{thread_id}.pdf"
    pdf.output(pdf_output_path)
    return FileResponse(pdf_output_path, filename=f"Guardian_Report_{thread_id}.pdf")

# --- Monetization (Stripe Mock) ---
@app.post("/api/checkout")
def create_checkout_session(current_user: User = Depends(get_current_user)):
    return {"url": "http://localhost:3000?payment_success=true"}

@app.post("/api/webhook/stripe_mock_success")
def stripe_mock_success(current_user: User = Depends(get_current_user)):
    try:
        supabase.auth.admin.update_user_by_id(current_user.id, {"user_metadata": {"is_pro": True}})
        return {"status": "upgraded to pro"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
