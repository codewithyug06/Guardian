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

    st.markdown("<br>### 🤖 AGENT SWARM", unsafe_allow_html=True)
    # Updated Agent List to include the new "Coder" agent
    agents = [
        ("Scout", "Discovery", "agent-active"), 
        ("Sentry", "Behavioral", "agent-active"), 
        ("Architect", "Financial", "agent-active"), 
        ("Coder", "Self-Healing", "agent-active"),  # <-- NEW AGENT
        ("Prophet", "Forecasting", "agent-active")
    ]
    for name, role, status_class in agents: st.markdown(f"<div style='margin-bottom:5px;'><span class='{status_class}'>●</span> <b>{name}</b> <span style='color:#666; font-size:0.8rem;'>// {role}</span></div>", unsafe_allow_html=True)
    
    st.markdown("<br>### 📟 LIVE AGENT LOGS", unsafe_allow_html=True)
    terminal_content = ""
    if "final_state" in st.session_state:
        # Filter detailed logs for display
        findings = st.session_state.final_state.get('findings', [])
        logs = [f"[{datetime.now().strftime('%H:%M:%S')}] SYS: {f}" for f in findings[-5:]]
        for log in logs: terminal_content += f"<div class='terminal-line'>{log}</div>"
    st.markdown(f"<div class='terminal-window'>{terminal_content}</div>", unsafe_allow_html=True)

# --- MAIN ACTION AREA ---
col_act1, col_act2, col_act3 = st.columns([2, 1, 4])
with col_act1:
    # 1. BUILD GRAPH
    graph = build_compliance_graph()
    
    # 2. CONFIGURATION (Unique Thread ID for Persistence)
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    # 3. CHECK STATUS (Is it paused at Visa Guard?)
    try:
        current_state = graph.get_state(config)
        # If next node is visa_guard, we are paused
        is_paused = bool(current_state.next and "visa_guard" in current_state.next)
    except:
        is_paused = False

    # 4. ACTION BUTTONS
    if is_paused:
        st.warning("⚠️ CRITICAL ACTION REQUIRED: Enforcement Pending Approval")
        
        # --- PHASE 2 FEATURE: SHOW GENERATED CODE PATCH ---
        # Retrieve the generated code from the Coder Agent (which ran before the pause)
        snapshot = graph.get_state(config)
        gen_code = snapshot.values.get("generated_code") if snapshot else None
        
        if gen_code:
            st.markdown("#### 🛠️ Proposed Self-Healing Patch (GenAI)")
            st.code(gen_code, language="python")

            # Split buttons: Apply Patch vs Just Block
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🔌 APPLY PATCH", type="primary", use_container_width=True):
                    st.toast("Patch Deployed to Production!", icon="🚀")
                    st.session_state.remediation_status = "COMPLETED"
                    time.sleep(1)
                    # We assume applying the patch is sufficient to resolve, but we can also rerender
                    st.rerun()

            with col_btn2:
                if st.button("🔓 APPROVE & RESUME", type="secondary", use_container_width=True):
                    with st.spinner("Executing Edge Enforcement..."):
                        final_state = graph.invoke(None, config)
                        st.session_state.final_state = final_state
                        st.rerun()
        else:
            # Fallback for Phase 1 (No Code)
            if st.button("🔓 APPROVE VISA GATEWAY BLOCK", type="primary", use_container_width=True):
                with st.spinner("Executing Edge Enforcement..."):
                    final_state = graph.invoke(None, config)
                    st.session_state.final_state = final_state
                    st.rerun()
                    
    else:
        if st.button("🚀 INITIALIZE STRATEGIC AUDIT", type="primary", use_container_width=True):
            st.session_state.remediation_status = "PENDING"
            with st.spinner("🤖 Agents Orchestrating (Scout Loop & Sentry Scan)..."):
                
                # INITIALIZE new run
                final_state = graph.invoke(
                    {"findings": [], "risk_level": "UNKNOWN", "scout_retries": 0}, 
                    config=config
                )
                
                # Check if we hit the pause (interrupt)
                snapshot = graph.get_state(config)
                if snapshot.next:
                    # We are paused -> store intermediate state
                    st.session_state.final_state = snapshot.values 
                    st.rerun()
                else:
                    # We finished -> store final state
                    st.session_state.final_state = final_state 
                    st.toast("Analysis Complete", icon="🛡️")

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

    # 1. HERO BANNER
    st.markdown("<br>", unsafe_allow_html=True)
    if is_paused:
        st.info("✋ SYSTEM PAUSED: Awaiting Human Authorization for Gateway Block.")
    elif remediated:
         st.success("✅ THREAT NEUTRALIZED: Policy Patched & Fines Averted.")
    else:
        visa_alert = next((f for f in reversed(state.get('findings', [])) if "VISA GATEWAY" in f), "System Warning")
        if "BLOCKED" in visa_alert:
            st.markdown(f"""<div class="critical-alert"><h3>⛔ VISA GATEWAY BLOCKED</h3><p>{visa_alert}</p></div>""", unsafe_allow_html=True)

    # 2. METRICS
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Systemic Risk Index", f"{current_risk_val}%", "-99%" if remediated else "+12%", delta_color="normal" if remediated else "inverse")
    with col2:
        st.metric("Est. Financial Liability", fine_val, "Liability Saved" if remediated else "Potential Fine", delta_color="inverse" if not remediated else "normal")
    with col3:
        status_text = "SECURE" if remediated else ("CRITICAL" if current_risk_val > 50 else "STABLE")
        st.metric("Compliance Posture", status_text, "Policy v2.2")

    # 3. VISUALIZATION & CHAT
    col_viz, col_chat = st.columns([1.5, 1])
    with col_viz:
        st.markdown("### 📈 RISK FORECAST")
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        risk_trend = [random.randint(0, 5) for _ in range(30)] if remediated else [min(100, x * 3 + random.randint(-5, 5)) for x in range(30)]
        fig = go.Figure(go.Scatter(x=dates, y=risk_trend, fill='tozeroy', line=dict(color='#00ff88' if remediated else '#ff0055')))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### ⚠️ STRATEGIC INTELLIGENCE")
        if remediated: st.success("Resolved: Policy updated.")
        else:
            for f in state.get('findings', []):
                # Highlight the RETRY (Reflection) step in the UI
                if "Retrying" in f: st.caption(f"🔄 {f}") 
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
        
        # Only show Auto-Remediate if NOT paused and risk is high
        if not remediated and current_risk_val > 50 and not is_paused:
             if st.button("⚡ EXECUTE AUTO-REMEDIATION", type="secondary", use_container_width=True):
                st.session_state.remediation_status = "COMPLETED"
                st.rerun()