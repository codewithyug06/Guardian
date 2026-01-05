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
import graphviz
from dotenv import load_dotenv
from core.graph import build_compliance_graph
from core.tools import generate_audit_report_text, _init_regulatory_graph

# 1. Load Environment Variables
load_dotenv()

# --- PAGE CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(
    page_title="GUARDIAN | Autonomous Governance",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# --- 🎨 THE "ELITE" DESIGN SYSTEM (CSS) ---
st.markdown("""
<style>
    /* FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    :root {
        --primary: #00f2ff;
        --secondary: #7000ff;
        --accent: #ff0055;
        --bg-dark: #050509;
        --glass: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.08);
        --text-main: #e0e6ed;
        --text-dim: #94a3b8;
    }

    /* GLOBAL RESET */
    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
        background-color: var(--bg-dark);
        color: var(--text-main);
    }

    /* --- SIDEBAR STYLING --- */
    [data-testid="stSidebar"] {
        background-color: #08080c;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] h1, h2, h3 {
        font-family: 'JetBrains Mono', monospace;
        color: var(--primary);
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.8;
    }

    /* --- METRIC CARDS (HUD STYLE) --- */
    .hud-card {
        background: linear-gradient(135deg, rgba(20,20,35,0.6) 0%, rgba(10,10,20,0.8) 100%);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        backdrop-filter: blur(12px);
    }
    .hud-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, var(--primary), transparent);
        opacity: 0.5;
    }
    .hud-card:hover {
        transform: translateY(-4px);
        border-color: var(--primary);
        box-shadow: 0 10px 30px -10px rgba(0, 242, 255, 0.2);
    }
    .hud-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.4rem;
        font-weight: 700;
        color: #fff;
        text-shadow: 0 0 15px rgba(255,255,255,0.1);
    }
    .hud-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--text-dim);
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* --- ALERTS & BANNERS --- */
    .alert-box {
        background: rgba(255, 0, 85, 0.1);
        border-left: 4px solid var(--accent);
        padding: 15px 20px;
        border-radius: 4px;
        margin: 10px 0;
        display: flex;
        align-items: flex-start;
        gap: 15px;
        animation: slideIn 0.5s ease-out;
    }
    .alert-title { font-weight: 700; color: #ff99bb; margin-bottom: 4px; font-family: 'JetBrains Mono'; }
    .alert-desc { font-size: 0.95rem; color: #ffccd5; }

    /* --- TERMINAL WINDOW --- */
    .terminal-container {
        background: #09090b;
        border: 1px solid #27272a;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        padding: 0;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    .terminal-header {
        background: #18181b;
        padding: 8px 15px;
        border-bottom: 1px solid #27272a;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #71717a;
        font-size: 0.75rem;
    }
    .terminal-body {
        padding: 15px;
        height: 350px;
        overflow-y: auto;
        color: #a1a1aa;
        line-height: 1.6;
    }
    .log-entry { margin-bottom: 8px; display: flex; gap: 10px; }
    .log-time { color: #52525b; }
    .log-system { color: var(--primary); }
    .log-alert { color: var(--accent); text-shadow: 0 0 8px rgba(255,0,85,0.4); }

    /* --- CHAT INTERFACE --- */
    .chat-container {
        background: #09090b;
        border: 1px solid #27272a;
        border-radius: 8px;
        height: 420px;
        display: flex;
        flex-direction: column;
    }
    .chat-messages {
        flex-grow: 1;
        overflow-y: auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    .msg { max-width: 85%; padding: 12px 16px; border-radius: 12px; font-size: 0.9rem; line-height: 1.5; }
    .msg-ai { align-self: flex-start; background: #18181b; border: 1px solid #27272a; color: #e4e4e7; border-bottom-left-radius: 2px; }
    .msg-user { align-self: flex-end; background: rgba(0, 242, 255, 0.1); border: 1px solid rgba(0, 242, 255, 0.2); color: #fff; border-bottom-right-radius: 2px; }
    
    /* --- CUSTOM SCROLLBAR --- */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #09090b; }
    ::-webkit-scrollbar-thumb { background: #27272a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #3f3f46; }

    /* ANIMATIONS */
    @keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    
    /* UTILS */
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .badge-active { background: rgba(0, 255, 136, 0.1); color: #00ff88; border: 1px solid rgba(0, 255, 136, 0.2); }
    .badge-inactive { background: rgba(255, 255, 255, 0.05); color: #666; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
c1, c2 = st.columns([0.8, 10])
with c1:
    st.markdown("<div style='font-size: 3.5rem; text-align: center; text-shadow: 0 0 20px rgba(0,242,255,0.5);'>🛡️</div>", unsafe_allow_html=True)
with c2:
    st.markdown("""
        <div style='margin-top: 5px;'>
            <h1 style='margin:0; font-size: 3rem; font-weight: 800; letter-spacing: -1px; background: linear-gradient(90deg, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                GUARD<span style='color: #00f2ff; text-shadow: 0 0 20px rgba(0,242,255,0.4); -webkit-text-fill-color: #00f2ff;'>IAN</span>
            </h1>
            <div style='display: flex; gap: 15px; align-items: center; margin-top: 5px;'>
                <span style='font-family: "JetBrains Mono"; font-size: 0.8rem; color: #64748b;'>AUTONOMOUS GOVERNANCE ECOSYSTEM</span>
                <span class="badge badge-active">● SYSTEM ONLINE</span>
                <span class="badge badge-active">V4.0.1 ELITE</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Initialize State
if "history" not in st.session_state: 
    st.session_state.history = [("ai", "Guardian System initialized. Monitoring active streams. Waiting for command...")]
if "remediation_status" not in st.session_state: st.session_state.remediation_status = "PENDING"
if "thread_id" not in st.session_state: st.session_state.thread_id = str(uuid.uuid4())

# --- SIDEBAR: COMMAND CENTER ---
with st.sidebar:
    st.markdown("### 🌐 JURISDICTION")
    jurisdiction = st.selectbox(
        "Label Hidden",
        ["Global (PCI-DSS)", "EU (GDPR)", "APAC (MAS)", "US (CCPA)"],
        label_visibility="collapsed"
    )
    st.caption(f"Current Framework: **{jurisdiction}**")
    
    st.markdown("---")
    st.markdown("### 👁️ OMNI-SENSOR INPUT")
    st.info("Drop Evidence Here (Img/Audio)")
    uploaded_evidence = st.file_uploader(
        "Hidden Label", 
        type=["png", "jpg", "jpeg", "mp3", "wav"], 
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ PROTOCOLS")
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        run_red_team = st.toggle("Red Team", value=False)
    with c_s2:
        use_fed_net = st.toggle("Fed. Net", value=False)
        
    st.markdown("---")
    st.markdown("### 🤖 SWARM NODES")
    
    agents_list = [
        ("Scout", "Discovery"), ("Ghost", "Red Team"), 
        ("Sentry", "Vision/ML"), ("Architect", "Strategy"), 
        ("Coder", "Patching"), ("Consensus", "Audit"), 
        ("Prophet", "Forecast")
    ]
    
    html_agents = "<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 8px;'>"
    for name, role in agents_list:
        active = name in ["Scout", "Sentry", "Architect"] # Simulating active state
        cls = "badge-active" if active else "badge-inactive"
        html_agents += f"<div class='badge {cls}' style='text-align:center;'>{name}</div>"
    html_agents += "</div>"
    st.markdown(html_agents, unsafe_allow_html=True)

# --- MAIN LOGIC ---

# CACHED GRAPH INITIALIZATION
@st.cache_resource
def get_graph():
    return build_compliance_graph()

graph = get_graph()
config = {"configurable": {"thread_id": st.session_state.thread_id}}

try:
    curr = graph.get_state(config)
    is_paused = bool(curr.next and "visa_guard" in curr.next)
except: is_paused = False

# --- DYNAMIC ACTION BANNER ---
if is_paused:
    snapshot = graph.get_state(config)
    gen_code = snapshot.values.get("generated_code")
    
    st.markdown(f"""
    <div class="alert-box" style="border-left-color: #ff0055; background: rgba(255, 0, 85, 0.05);">
        <div style="font-size: 1.5rem;">⚠️</div>
        <div>
            <div class="alert-title">CRITICAL INTERVENTION REQUIRED</div>
            <div class="alert-desc">The Architect Agent has generated a self-healing patch. Authorization required to deploy to production.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_code, col_act = st.columns([1.5, 1])
    with col_code:
        st.markdown("##### 🧬 GENERATED PATCH PREVIEW")
        st.code(gen_code, language="python")
    with col_act:
        st.markdown("##### 🛡️ DECISION MATRIX")
        st.info(snapshot.values.get("remediation_plan", "No plan."))
        
        b1, b2 = st.columns(2)
        if b1.button("⚡ DEPLOY PATCH", type="primary", use_container_width=True):
            st.session_state.remediation_status = "COMPLETED"
            st.rerun()
        if b2.button("🚫 BLOCK ONLY", type="secondary", use_container_width=True):
            with st.spinner("Enforcing Edge Block..."):
                final = graph.invoke(None, config)
                st.session_state.final_state = final
                st.rerun()

else:
    # --- CONTROL BAR ---
    c_btn, c_stat = st.columns([1, 4])
    with c_btn:
        label = "🔥 LAUNCH ATTACK" if run_red_team else "🚀 START AUDIT"
        kind = "secondary" if run_red_team else "primary"
        
        if st.button(label, type=kind, use_container_width=True):
            st.session_state.remediation_status = "PENDING"
            with st.spinner("🔄 ORCHESTRATING SWARM AGENTS..."):
                # Intelligent File Handling
                img, aud = None, None
                if uploaded_evidence:
                    if uploaded_evidence.type.startswith('image'): img = uploaded_evidence.getvalue()
                    elif uploaded_evidence.type.startswith('audio'): aud = uploaded_evidence.getvalue()

                inputs = {
                    "findings": [], "risk_level": "UNKNOWN", "scout_retries": 0,
                    "red_team_mode": run_red_team, "federated_mode": use_fed_net,
                    "uploaded_image_bytes": img, "audio_bytes": aud, "jurisdiction": jurisdiction
                }
                final = graph.invoke(inputs, config=config)
                snapshot = graph.get_state(config)
                if snapshot.next:
                    st.session_state.final_state = snapshot.values 
                    st.rerun()
                else:
                    st.session_state.final_state = final

# --- METRICS HUD ---
if "final_state" in st.session_state:
    state = st.session_state.final_state
    remediated = st.session_state.remediation_status == "COMPLETED"
    
    # Calc logic
    if remediated:
        risk, fine, drift = 0, "$0.00", 0.0
        status = "SECURE"
    else:
        risk = 99 if state.get('risk_level') in ["HIGH", "CRITICAL"] else 12
        fine = "$100,000"
        drift = state.get("compliance_drift", 0.0)
        status = state.get('risk_level', "UNKNOWN")
        
        for gap in state.get('policy_gaps', []):
            if "ESTIMATED LIABILITY" in gap: fine = gap.split("LIABILITY:")[-1].strip().split("/")[0]

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    
    def hud(label, val, sub, color):
        return f"""
        <div class="hud-card">
            <div class="hud-label"><span>{label}</span></div>
            <div class="hud-value" style="color: {color}">{val}</div>
            <div style="font-size: 0.8rem; color: #64748b; margin-top: 5px;">{sub}</div>
        </div>
        """
    
    color_risk = "#ff0055" if risk > 50 else "#00ff88"
    with m1: st.markdown(hud("SYSTEMIC RISK", f"{risk}%", "Real-time Inference", color_risk), unsafe_allow_html=True)
    with m2: st.markdown(hud("LIABILITY EXPOSURE", fine, "Projected Monthly Fine", "#e0e6ed"), unsafe_allow_html=True)
    with m3: st.markdown(hud("COMPLIANCE DRIFT", f"{drift}%", "Baseline Deviation", "#ffaa00" if drift > 20 else "#00ff88"), unsafe_allow_html=True)
    with m4: st.markdown(hud("POSTURE STATUS", status, f"Policy v2.4 ({jurisdiction.split()[0]})", color_risk), unsafe_allow_html=True)

    # --- MAIN CONTENT TABS ---
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["📈 LIVE INTEL", "🕸️ NEURAL MESH", "🔒 AUDIT VAULT"])

    with t1:
        c1, c2 = st.columns([2, 1])
        with c1:
            dates = [datetime.now() + timedelta(days=x) for x in range(30)]
            forecast = state.get("risk_forecast", [])
            if not forecast or remediated: forecast = [random.randint(0, 5) for _ in range(30)]
            
            fig = go.Figure(go.Scatter(x=dates, y=forecast, fill='tozeroy', line=dict(color='#00ff88' if remediated else '#ff0055', width=3)))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                height=300, margin=dict(l=0,r=0,t=20,b=20),
                xaxis=dict(showgrid=False, color='#444'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#444')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with c2:
            st.markdown("##### ⚡ ACTIVE THREAT STREAM")
            if remediated:
                st.success("✔ System Secured. No active threats.")
            else:
                findings = state.get('findings', [])
                if not findings: st.info("No anomalies detected.")
                for f in findings:
                    if "FED-NET" in f: st.markdown(f"<div style='color:#00ff88; font-size:0.85rem; margin-bottom:8px;'>🌐 {f}</div>", unsafe_allow_html=True)
                    elif "GHOST" in f: st.markdown(f"<div style='color:#ff0055; font-size:0.85rem; margin-bottom:8px;'>💀 {f}</div>", unsafe_allow_html=True)
                    elif "VISION" in f: st.markdown(f"<div style='color:#ffaa00; font-size:0.85rem; margin-bottom:8px;'>👁️ {f}</div>", unsafe_allow_html=True)
                    elif "SAFE MODE" in f: st.markdown(f"<div style='color:#ff0055; font-weight:bold; font-size:0.85rem; margin-bottom:8px;'>⛔ {f}</div>", unsafe_allow_html=True)
                    else: st.markdown(f"<div style='color:#ccc; font-size:0.85rem; margin-bottom:8px;'>• {f}</div>", unsafe_allow_html=True)

    with t2:
        st.markdown("##### 🔗 KNOWLEDGE GRAPH TOPOLOGY")
        st.info("ℹ️ Mesh RAG Visualization: This graph demonstrates how a failure in PCI-DSS Requirement 3.4 semantically triggers a GDPR Article 32 risk because they share the 'Encryption' concept node.")
        try:
            graph = graphviz.Digraph()
            graph.attr(bgcolor='transparent')
            G = _init_regulatory_graph()
            for n in G.nodes:
                c = "#ff0055" if G.nodes[n].get('type') == "Regulation" else "#00f2ff"
                graph.node(str(n), style="filled", fillcolor="#0d1117", fontcolor="white", color=c, penwidth="2")
            for e in G.edges:
                graph.edge(str(e[0]), str(e[1]), color="#333", penwidth="1")
            st.graphviz_chart(graph)
        except: st.caption("Visual Engine Loading...")

    with t3:
        c_a, c_b = st.columns(2)
        with c_a:
            st.markdown("##### 🤝 SWARM CONSENSUS")
            audit_logs = state.get("consensus_audit", [])
            if audit_logs:
                for l in audit_logs:
                    if "✅" in l: st.success(l)
                    elif "❌" in l: st.error(l)
                    else: st.info(l)
            else: st.caption("No active consensus protocols.")
        
        with c_b:
            st.markdown("##### 📄 GENERATE REPORT")
            rpt = generate_audit_report_text(state)
            st.download_button("DOWNLOAD ENCRYPTED REPORT", rpt, "audit.txt", "text/plain", type="primary", use_container_width=True)

    # --- FOOTER: TERMINAL & CHAT ---
    st.markdown("---")
    col_term, col_chat = st.columns([1.2, 1])
    
    with col_term:
        st.markdown("### 📟 SYSTEM TERMINAL")
        term_html = """
        <div class='terminal-container'>
            <div class='terminal-header'>
                <span>root@guardian-core:~#</span>
                <span style='margin-left:auto'>● LIVE</span>
            </div>
            <div class='terminal-body'>
        """
        findings = state.get('findings', [])
        if not findings: term_html += "<div class='log-entry'><span class='log-time'>--:--:--</span> <span class='log-system'>System Ready. Waiting for input stream...</span></div>"
        
        for f in findings:
            ts = datetime.now().strftime('%H:%M:%S')
            style = "log-alert" if "ALERT" in f or "CRITICAL" in f else "log-system"
            term_html += f"<div class='log-entry'><span class='log-time'>{ts}</span> <span class='{style}'>{f}</span></div>"
        
        term_html += "</div></div>"
        st.markdown(term_html, unsafe_allow_html=True)

    with col_chat:
        st.markdown("### 💬 GUARDIAN ASSISTANT")
        
        # Display Chat History
        chat_html = "<div class='chat-container'><div class='chat-messages'>"
        for role, msg in st.session_state.history:
            cls = "msg-user" if role == "user" else "msg-ai"
            chat_html += f"<div class='msg {cls}'>{msg}</div>"
        chat_html += "</div></div>"
        st.markdown(chat_html, unsafe_allow_html=True)
        
        # Input Area (Sticky Bottom feel via Columns)
        input_c1, input_c2 = st.columns([4, 1])
        with input_c1:
            q = st.text_input("Message Guardian...", label_visibility="collapsed", placeholder="Ask about the audit results...")
        with input_c2:
            if st.button("SEND", type="primary", use_container_width=True) and q:
                st.session_state.history.append(("user", q))
                st.session_state.history.append(("ai", "I've analyzed the latest telemetry. The Scout agent successfully identified the regulatory gap, and the Architect has mapped it to a financial liability of $100k."))
                st.rerun()