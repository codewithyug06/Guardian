import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
import uuid
from dotenv import load_dotenv
from core.graph import build_compliance_graph

# 1. Load Environment Variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AegisFlow | Strategic Intelligence",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# --- THE "WORLD CLASS" CSS INJECTION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; }
    .stApp { background-color: #050505; background-image: radial-gradient(circle at 50% 0%, #1a1a40 0%, #050505 70%); color: #e0e0e0; }
    .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); margin-bottom: 20px; }
    @keyframes border-glow { 0% { border-color: rgba(255, 0, 85, 0.4); box-shadow: 0 0 10px rgba(255, 0, 85, 0.2); } 50% { border-color: rgba(255, 0, 85, 1); box-shadow: 0 0 20px rgba(255, 0, 85, 0.6); } 100% { border-color: rgba(255, 0, 85, 0.4); box-shadow: 0 0 10px rgba(255, 0, 85, 0.2); } }
    .critical-alert { background: rgba(40, 0, 10, 0.6); border: 2px solid #ff0055; animation: border-glow 2s infinite; border-radius: 12px; padding: 15px; color: #ff99bb; }
    [data-testid="stMetricValue"] { font-family: 'Rajdhani', sans-serif !important; font-size: 3rem !important; font-weight: 700 !important; text-shadow: 0 0 10px rgba(0, 242, 255, 0.3); }
    [data-testid="stSidebar"] { background-color: #0a0a0c; border-right: 1px solid #1f2937; }
    .agent-active { color: #00f2ff; text-shadow: 0 0 8px #00f2ff; }
    .terminal-window { background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 10px; font-family: 'Courier New', monospace; font-size: 0.8rem; color: #58a6ff; height: 150px; overflow-y: auto; margin-top: 10px; }
    .terminal-line { margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

# --- HEADER WITH LOGO ---
col_head1, col_head2 = st.columns([0.8, 10])
with col_head1: st.markdown("<h1>🛡️</h1>", unsafe_allow_html=True)
with col_head2:
    st.markdown("<h1 style='margin-bottom:0; color:#fff;'>AEGIS<span style='color:#00f2ff'>FLOW</span> <span style='font-size:1.2rem; color:#666; font-weight:400;'>| Strategic Risk Intelligence</span></h1>", unsafe_allow_html=True)
    st.markdown("<div style='color:#888; font-size:0.9rem; letter-spacing:1px;'>REAL-TIME • BEHAVIORAL • PREDICTIVE • SELF-HEALING</div>", unsafe_allow_html=True)

st.markdown("---")

# Initialize Session State
if "history" not in st.session_state: st.session_state.history = []
if "remediation_status" not in st.session_state: st.session_state.remediation_status = "PENDING"
if "audit_log" not in st.session_state: st.session_state.audit_log = []
if "thread_id" not in st.session_state: st.session_state.thread_id = str(uuid.uuid4())

# --- SIDEBAR: THE COMMAND RAIL ---
with st.sidebar:
    st.markdown("### 📡 SYSTEM STATUS")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key: st.markdown("<div style='color:#ffaa00; font-weight:bold; border:1px solid #ffaa00; padding:8px; border-radius:4px;'>⚠️ CIRCUIT BREAKER ACTIVE</div>", unsafe_allow_html=True)
    else: st.markdown("<div style='color:#00ff88; font-weight:bold; border:1px solid #00ff88; padding:8px; border-radius:4px;'>✅ CORE SYSTEMS ONLINE</div>", unsafe_allow_html=True)

    st.markdown("<br>### 👁️ VISUAL SENTRY", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Dashboard Screenshot", type=["png", "jpg", "jpeg"])

    st.markdown("<br>### ⚔️ ADVERSARIAL GOVERNANCE", unsafe_allow_html=True)
    # NEW RED TEAM BUTTON
    run_red_team = st.button("🔥 RUN RED TEAM STRESS TEST", type="secondary", use_container_width=True)

    st.markdown("<br>### 🤖 AGENT SWARM", unsafe_allow_html=True)
    agents = ["Scout", "Ghost", "Sentry", "Architect", "Coder", "Prophet"]
    for name in agents: st.markdown(f"<div><span class='agent-active'>●</span> <b>{name}</b></div>", unsafe_allow_html=True)
    
    st.markdown("<br>### 📟 LIVE AGENT LOGS", unsafe_allow_html=True)
    terminal_content = ""
    if "final_state" in st.session_state:
        findings = st.session_state.final_state.get('findings', [])
        logs = [f"[{datetime.now().strftime('%H:%M:%S')}] SYS: {f}" for f in findings[-6:]]
        for log in logs: terminal_content += f"<div class='terminal-line'>{log}</div>"
    st.markdown(f"<div class='terminal-window'>{terminal_content}</div>", unsafe_allow_html=True)

# --- MAIN ACTION AREA ---
col_act1, col_act2, col_act3 = st.columns([2, 1, 4])
with col_act1:
    graph = build_compliance_graph()
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    try:
        current_state = graph.get_state(config)
        is_paused = bool(current_state.next and "visa_guard" in current_state.next)
    except:
        is_paused = False

    if is_paused:
        st.warning("⚠️ CRITICAL ACTION REQUIRED: Enforcement Pending Approval")
        
        snapshot = graph.get_state(config)
        gen_code = snapshot.values.get("generated_code")
        
        if gen_code:
            st.markdown("#### 🛠️ Proposed Self-Healing Patch (GenAI)")
            st.code(gen_code, language="python")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔌 APPLY PATCH", type="primary", use_container_width=True):
                 st.toast("Patch Deployed to Production!")
                 st.session_state.remediation_status = "COMPLETED"
                 time.sleep(1)
                 st.rerun()
                 
        with col_btn2:
            if st.button("🔓 APPROVE & RESUME", type="secondary", use_container_width=True):
                with st.spinner("Executing Edge Enforcement..."):
                    final_state = graph.invoke(None, config)
                    st.session_state.final_state = final_state
                    st.rerun()
    else:
        # Determine Trigger Source (Button or Default)
        if run_red_team:
            st.session_state.remediation_status = "PENDING"
            with st.spinner("⚔️ RED TEAM ATTACK LAUNCHED..."):
                inputs = {
                    "findings": [], "risk_level": "UNKNOWN", "scout_retries": 0,
                    "red_team_mode": True, # ACTIVATE GHOST
                    "uploaded_image_bytes": None
                }
                final = graph.invoke(inputs, config=config)
                # Store and rerun to show results
                snapshot = graph.get_state(config)
                if snapshot.next: st.session_state.final_state = snapshot.values
                else: st.session_state.final_state = final
                st.rerun()

        elif st.button("🚀 INITIALIZE STRATEGIC AUDIT", type="primary", use_container_width=True):
            st.session_state.remediation_status = "PENDING"
            with st.spinner("🤖 Agents Orchestrating..."):
                inputs = {
                    "findings": [], "risk_level": "UNKNOWN", "scout_retries": 0,
                    "red_team_mode": False, # NORMAL MODE
                    "uploaded_image_bytes": uploaded_file.getvalue() if uploaded_file else None
                }
                final = graph.invoke(inputs, config=config)
                
                snapshot = graph.get_state(config)
                if snapshot.next:
                    st.session_state.final_state = snapshot.values
                    st.rerun()
                else:
                    st.session_state.final_state = final

# --- DASHBOARD LAYOUT ---
if "final_state" in st.session_state:
    state = st.session_state.final_state
    remediated = st.session_state.remediation_status == "COMPLETED"

    # DATA PROCESSING
    if remediated:
        current_risk_val = 0
        fine_val = "$0.00"
    else:
        current_risk_val = 99 if state.get('risk_level') in ["HIGH", "CRITICAL"] else 15
        fine_val = "$100,000/mo"
        for gap in state.get('policy_gaps', []):
            if "ESTIMATED LIABILITY" in gap: fine_val = gap.split("LIABILITY:")[-1].strip()

    st.markdown("<br>", unsafe_allow_html=True)
    if is_paused:
        st.info("✋ SYSTEM PAUSED: Awaiting Approval for Patch & Gateway Block.")
    elif remediated:
         st.success("✅ THREAT NEUTRALIZED: Policy Patched & Fines Averted.")
    else:
        visa_alert = next((f for f in reversed(state.get('findings', [])) if "VISA GATEWAY" in f), "System Warning")
        if "BLOCKED" in visa_alert:
            st.markdown(f"""<div class="critical-alert"><h3>⛔ VISA GATEWAY BLOCKED</h3><p>{visa_alert}</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Systemic Risk Index", f"{current_risk_val}%", "-99%" if remediated else "+12%", delta_color="normal" if remediated else "inverse")
    with col2:
        st.metric("Est. Financial Liability", fine_val, "Liability Saved" if remediated else "Potential Fine", delta_color="inverse" if not remediated else "normal")
    with col3:
        status_text = "SECURE" if remediated else ("CRITICAL" if current_risk_val > 50 else "STABLE")
        st.metric("Compliance Posture", status_text, "Policy v2.2")

    col_viz, col_chat = st.columns([1.5, 1])
    with col_viz:
        st.markdown("### 📈 PROPHET FORECAST (Real-Time)")
        
        dates = [datetime.now() + timedelta(days=x) for x in range(30)]
        forecast_data = state.get("risk_forecast", [])
        
        if not forecast_data or remediated:
             forecast_data = [random.randint(0, 5) for _ in range(30)]
             line_color = '#00ff88'
        else:
             line_color = '#ff0055'

        fig = go.Figure(go.Scatter(x=dates, y=forecast_data, fill='tozeroy', line=dict(color=line_color)))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### ⚠️ STRATEGIC INTELLIGENCE")
        if remediated: st.success("Resolved: Policy updated.")
        else:
            for f in state.get('findings', []):
                # Phase 7 Update: Highlighting Ghost Attacks
                if "GHOST" in f: st.error(f"**{f}**", icon="💀") # Ghost Alert
                elif "VISION SENTRY" in f: st.error(f"**{f}**", icon="👁️")
                elif "Retrying" in f: st.caption(f"🔄 {f}") 
                elif "BEHAVIORAL" in f: st.warning(f"**{f}**", icon="⚡")
                
            for gap in state.get('policy_gaps', []):
                 if "ESTIMATED LIABILITY" not in gap: st.warning(f"**Violation:** {gap}", icon="⚠️")

    with col_chat:
        st.markdown("### 💬 AEGIS ASSISTANT")
        chat_container = st.container(height=300)
        user_query = st.chat_input("Query Agent Swarm...")
        if user_query:
            st.session_state.history.append(("user", user_query))
            st.session_state.history.append(("ai", "Analyze the 'Scout' logs. You will see it self-corrected before finding the result."))
        with chat_container:
            for role, msg in st.session_state.history:
                st.markdown(f"<div class='{'user-msg' if role=='user' else 'ai-msg'}'>{msg}</div>", unsafe_allow_html=True)
        
        if not remediated and current_risk_val > 50 and not is_paused:
             if st.button("⚡ EXECUTE AUTO-REMEDIATION", type="secondary", use_container_width=True):
                st.session_state.remediation_status = "COMPLETED"
                st.rerun()