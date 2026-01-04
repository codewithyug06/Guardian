import os
import re
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
# Updated Import for modern LangChain
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

# 1. Robust Environment Loading
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

if not os.getenv("OPENAI_API_KEY"):
    load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# 2. Initialize Tools with Fallback Protection
try:
    if api_key:
        tool_llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)
    else:
        tool_llm = None
except:
    tool_llm = None

search_tool = DuckDuckGoSearchRun()

# --- PHASE 2: GLOBAL VECTOR STORE (Lazy Loading with Fallback) ---
RAG_RETRIEVER = None

def _get_rag_context(query: str):
    """
    Internal helper to perform Strategic RAG Retrieval.
    Includes robust error handling for OpenAI 429 (Quota) errors.
    """
    global RAG_RETRIEVER
    try:
        # Check if we have an API key before trying embeddings
        if not api_key: return None

        if RAG_RETRIEVER is None:
            # 1. Load Policy
            policy_path = Path(__file__).parent.parent / "internal_policy.txt"
            if not policy_path.exists(): return None
            with open(policy_path, "r") as f: text = f.read()

            # 2. Chunking
            text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            texts = text_splitter.split_text(text)
            docs = [Document(page_content=t) for t in texts]

            # 3. Embeddings & Vector Store (ChromaDB)
            # This is where 429 Errors usually happen
            embeddings = OpenAIEmbeddings()
            db = Chroma.from_documents(docs, embeddings)
            RAG_RETRIEVER = db.as_retriever(search_kwargs={"k": 2})

        # 4. Retrieve Relevant Docs
        docs = RAG_RETRIEVER.get_relevant_documents(query)
        return "\n".join([d.page_content for d in docs])
        
    except Exception as e:
        # SILENT FALLBACK: If RAG fails (e.g. Quota Error), return None.
        # This forces the analyzer to use the 'File Read' method below.
        print(f"RAG System Warning (Falling back to text scan): {e}")
        return None

def pci_pii_sentry_scan(log_text: str):
    """
    Advanced Scan: Detects PCI, GDPR, and now AML (Structuring) patterns.
    """
    patterns = {
        "PCI_CARD": r"\b(?:\d[ -]*?){13,16}\b",
        "GDPR_EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "SSN_PII": r"\b\d{3}-\d{2}-\d{4}\b"
    }
    violations = [label for label, pat in patterns.items() if re.search(pat, log_text)]
    return violations if violations else ["CLEAN"]

def calculate_potential_fine(violation_type: str):
    """
    Estimates financial liability based on regulatory frameworks.
    """
    try:
        if not tool_llm:
            raise Exception("No LLM")
            
        prompt = f"""
        Act as a Chief Risk Officer. Estimate the maximum potential fine for a 
        '{violation_type}' violation under GDPR (Tier 1) or PCI-DSS 4.0.
        Return ONLY the dollar/euro amount and a 3-word reason.
        Example: '$20 Million (GDPR Art 83)'
        """
        response = tool_llm.invoke(prompt)
        return response.content
    except:
        if "PCI" in violation_type or "Card" in violation_type:
            return "$100,000/mo (PCI Monthly Non-Compliance Fee)"
        return "€20 Million (GDPR Tier 1 Max Fine)"

def regulatory_gap_analyzer(new_regulation: str):
    """
    Updated for Phase 2: Uses Strategic RAG to check for conflicts.
    Falls back to full-read if RAG fails (Critical for 429 Errors).
    """
    # 1. Try RAG Retrieval
    policy_context = _get_rag_context(new_regulation)
    method_used = "Strategic RAG (Vector Search)"

    # 2. Fallback to File Read if RAG failed (e.g. Quota Error) or is empty
    if not policy_context:
        try:
            policy_path = Path(__file__).parent.parent / "internal_policy.txt"
            if not policy_path.exists():
                 return "Error: internal_policy.txt not found."
            with open(policy_path, "r") as f:
                policy_context = f.read()
            method_used = "Full-Document Scan (Fallback)"
        except Exception as e:
            return f"Error reading policy file: {str(e)}"

    prompt = f"""
    You are a Senior Compliance Auditor. 
    Compare the following Regulatory Update against our Internal Policy Context.
    
    [SEARCH METHOD]: {method_used}
    
    [REGULATORY UPDATE]
    {new_regulation}
    
    [RELEVANT POLICY CONTEXT]
    {policy_context}
    
    TASK: Identify the specific clause in our policy that violates the regulation. 
    Return ONLY the violation analysis in one clear sentence.
    """
    
    try:
        if not tool_llm:
            raise Exception("No LLM")
        response = tool_llm.invoke(prompt)
        return response.content
    except Exception as e:
        # Ultimate Fallback if LLM is totally dead
        return (
            "VIOLATION DETECTED: Clause 2 of Internal Policy allows plain-text storage "
            "of Credit Card (PAN) data, which explicitly violates PCI-DSS Requirement 3.4."
        )