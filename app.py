import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
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
    /* IMPORT FUTURISTIC FONT */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');

    /* GLOBAL THEME */
    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a40 0%, #050505 70%);
        color: #e0e0e0;
    }

    /* GLASSMORPHISM CARD STYLE */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }

    /* GLOWING BORDER ANIMATION FOR CRITICAL ALERTS */
    @keyframes border-glow {
        0% { border-color: rgba(255, 0, 85, 0.4); box-shadow: 0 0 10px rgba(255, 0, 85, 0.2); }
        50% { border-color: rgba(255, 0, 85, 1); box-shadow: 0 0 20px rgba(255, 0, 85, 0.6); }
        100% { border-color: rgba(255, 0, 85, 0.4); box-shadow: 0 0 10px rgba(255, 0, 85, 0.2); }
    }

    .critical-alert {
        background: rgba(40, 0, 10, 0.6);
        border: 2px solid #ff0055;
        animation: border-glow 2s infinite;
        border-radius: 12px;
        padding: 15px;
        color: #ff99bb;
    }
    
    /* CUSTOM METRICS */
    [data-testid="stMetricValue"] {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
    }
    [data-testid="stMetricLabel"] {
        color: #8899a6 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #0a0a0c;
        border-right: 1px solid #1f2937;
    }
    
    /* AGENT STATUS DOTS */
    .agent-active { color: #00f2ff; text-shadow: 0 0 8px #00f2ff; }
    .agent-critical { color: #ff0055; text-shadow: 0 0 8px #ff0055; }
    
    /* BUTTON STYLING */
    .stButton > button {
        background: linear-gradient(90deg, #00f2ff 0%, #0078ff 100%);
        color: #000;
        font-weight: 800;
        border: none;
        border-radius: 6px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.5);
    }
    
    /* CHAT BUBBLES */
    .user-msg {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        border-left: 4px solid #00f2ff;
        padding: 15px;
        border-radius: 0 12px 12px 12px;
        margin-bottom: 15px;
        color: #fff;
    }
    .ai-msg {
        background: linear-gradient(135deg, #001f3f 0%, #000810 100%);
        border-left: 4px solid #ff0055;
        padding: 15px;
        border-radius: 0 12px 12px 12px;
        margin-bottom: 15px;
        color: #e0f0ff;
        box-shadow: inset 0 0 20px rgba(0, 78, 152, 0.2);
    }

    /* TERMINAL STYLE */
    .terminal-window {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
        color: #58a6ff;
        height: 150px;
        overflow-y: auto;
        margin-top: 10px;
    }
    .terminal-line { margin-bottom: 4px; }
    .terminal-cursor { display: inline-block; width: 8px; height: 15px; background: #58a6ff; animation: blink 1s infinite; }
    @keyframes blink { 50% { opacity: 0; } }

</style>
""", unsafe_allow_html=True)

# --- HEADER WITH LOGO ---
col_head1, col_head2 = st.columns([0.8, 10])
with col_head1:
    st.markdown("<h1>🛡️</h1>", unsafe_allow_html=True)
with col_head2:
    st.markdown("<h1 style='margin-bottom:0; color:#fff;'>AEGIS<span style='color:#00f2ff'>FLOW</span> <span style='font-size:1.2rem; color:#666; font-weight:400;'>| Strategic Risk Intelligence</span></h1>", unsafe_allow_html=True)
    st.markdown("<div style='color:#888; font-size:0.9rem; letter-spacing:1px;'>REAL-TIME • BEHAVIORAL • PREDICTIVE • SELF-HEALING</div>", unsafe_allow_html=True)

st.markdown("---")

# Initialize Session State
if "history" not in st.session_state: st.session_state.history = []
if "remediation_status" not in st.session_state: st.session_state.remediation_status = "PENDING"
if "audit_log" not in st.session_state: st.session_state.audit_log = []

# --- SIDEBAR: THE COMMAND RAIL ---
with st.sidebar:
    st.markdown("### 📡 SYSTEM STATUS")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.markdown("<div style='color:#ffaa00; font-weight:bold; border:1px solid #ffaa00; padding:8px; border-radius:4px;'>⚠️ CIRCUIT BREAKER ACTIVE</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#00ff88; font-weight:bold; border:1px solid #00ff88; padding:8px; border-radius:4px;'>✅ CORE SYSTEMS ONLINE</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🤖 AGENT SWARM")
    
    # Custom HTML for Agents
    agents = [
        ("Scout", "Discovery", "agent-active"),
        ("Sentry", "Behavioral", "agent-active"),
        ("Architect", "Financial", "agent-active"),
        ("Prophet", "Forecasting", "agent-active")
    ]
    
    for name, role, status_class in agents:
        st.markdown(f"<div style='margin-bottom:5px;'><span class='{status_class}'>●</span> <b>{name}</b> <span style='color:#666; font-size:0.8rem;'>// {role}</span></div>", unsafe_allow_html=True)
    
    # Visa Guard Dynamic Status
    st.markdown("<br>", unsafe_allow_html=True)
    if "final_state" in st.session_state:
        if st.session_state.remediation_status == "COMPLETED":
             st.markdown("<div style='background:#0a2010; padding:10px; border-radius:8px; border:1px solid #00ff88; color:#00ff88;'>🔒 <b>VISA GUARD: SECURE</b></div>", unsafe_allow_html=True)
        elif st.session_state.final_state.get('risk_level') in ["HIGH", "CRITICAL"]:
            st.markdown("<div style='background:#2a0505; padding:10px; border-radius:8px; border:1px solid #ff0055; color:#ff0055; animation: border-glow 2s infinite;'>⛔ <b>VISA GUARD: ENFORCING</b></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background:#20200a; padding:10px; border-radius:8px; border:1px solid #ffaa00; color:#ffaa00;'>⏳ <b>VISA GUARD: STANDBY</b></div>", unsafe_allow_html=True)

    # LIVE TERMINAL SIMULATION
    st.markdown("<br>### 📟 LIVE AGENT LOGS", unsafe_allow_html=True)
    
    # Fake terminal logs for ambiance
    terminal_content = ""
    if "final_state" in st.session_state:
        logs = [
            f"[{datetime.now().strftime('%H:%M:%S')}] SCOUT: Scanning PCI-DSS v4.0...",
            f"[{datetime.now().strftime('%H:%M:%S')}] SENTRY: Packet stream analyzed. 150ms latency.",
            f"[{datetime.now().strftime('%H:%M:%S')}] ARCHITECT: Calculating financial exposure...",
            f"[{datetime.now().strftime('%H:%M:%S')}] PROPHET: Running Monte Carlo simulation..."
        ]
        if st.session_state.remediation_status == "COMPLETED":
             logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] SYS: PATCH APPLIED. REBOOTING...")
        for log in logs:
            terminal_content += f"<div class='terminal-line'>{log}</div>"
            
    st.markdown(f"<div class='terminal-window'>{terminal_content}<span class='terminal-cursor'></span></div>", unsafe_allow_html=True)

# --- MAIN ACTION AREA ---
col_act1, col_act2, col_act3 = st.columns([2, 1, 4])
with col_act1:
    if st.button("🚀 INITIALIZE STRATEGIC AUDIT", type="primary", use_container_width=True):
        st.session_state.remediation_status = "PENDING"
        engine = build_compliance_graph()
        
        # Custom Progress Bar
        progress_text = "Agents Orchestrating..."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.01) # Fake processing time for UI drama
            my_bar.progress(percent_complete + 1, text=f"Agents Thinking... {percent_complete}%")
            
        final_state = engine.invoke({"findings": [], "risk_level": "UNKNOWN", "policy_gaps": []})
        st.session_state.final_state = final_state 
        my_bar.empty()
        st.toast("Strategic Analysis Complete", icon="🛡️")

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
        # Fallback Fine Value
        fine_val = "$100,000/mo"
        for gap in state.get('policy_gaps', []):
            if "ESTIMATED LIABILITY" in gap:
                fine_val = gap.split("LIABILITY:")[-1].strip()

    # 1. THE HERO BANNER (Animated Critical Alert)
    st.markdown("<br>", unsafe_allow_html=True)
    if remediated:
        st.markdown("""
        <div style="background: rgba(0, 255, 136, 0.1); border: 1px solid #00ff88; padding: 20px; border-radius: 12px; display: flex; align-items: center;">
            <div style="font-size: 2rem; margin-right: 15px;">✅</div>
            <div>
                <h3 style="margin: 0; color: #00ff88;">THREAT NEUTRALIZED</h3>
                <p style="margin: 0; color: #ccc;">Policy Patched • Fines Averted • Gateway Unlocked</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        visa_alert = next((f for f in reversed(state['findings']) if "VISA GATEWAY" in f), "System Warning")
        if "BLOCKED" in visa_alert:
            st.markdown(f"""
            <div class="critical-alert" style="display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 15px;">⛔</div>
                <div>
                    <h3 style="margin: 0; color: #ff0055;">VISA GATEWAY BLOCKED</h3>
                    <p style="margin: 0; color: #ffcccc;">{visa_alert}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 2. METRICS ROW (Glassmorphism Cards)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        delta_color = "normal" if remediated else ("inverse" if current_risk_val > 50 else "normal")
        st.metric("Systemic Risk Index", f"{current_risk_val}%", 
                  "-99% (Secure)" if remediated else "+12% (Rising)",
                  delta_color=delta_color)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fine_color = "inverse" if not remediated else "normal"
        st.metric("Est. Financial Liability", fine_val, "Liability Saved" if remediated else "Potential Fine", delta_color=fine_color)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        status_text = "SECURE" if remediated else ("CRITICAL" if current_risk_val > 50 else "STABLE")
        st.metric("Compliance Posture", status_text, "Policy v2.2" if remediated else "Policy v2.1")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. SPLIT VIEW: CHART vs CHAT
    col_viz, col_chat = st.columns([1.5, 1])

    with col_viz:
        st.markdown("### 📈 RISK FORECAST (30 DAYS)")
        
        # Prophet Chart Logic
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        if remediated:
            risk_trend = [random.randint(0, 5) for _ in range(30)]
            fill_color = 'rgba(0, 255, 136, 0.2)'
            line_color = '#00ff88'
        else:
            risk_trend = [min(100, x * 3 + random.randint(-5, 5)) for x in range(30)]
            fill_color = 'rgba(255, 0, 85, 0.2)'
            line_color = '#ff0055'
        
        # Advanced Plotly Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=risk_trend,
            fill='tozeroy',
            mode='lines',
            line=dict(color=line_color, width=3),
            fillcolor=fill_color
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0),
            height=250,
            xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='#666')),
            yaxis=dict(showgrid=True, gridcolor='#333', tickfont=dict(color='#666'))
        )
        st.plotly_chart(fig, use_container_width=True)

        # INTELLIGENCE CARDS
        st.markdown("### ⚠️ STRATEGIC INTELLIGENCE")
        if remediated:
            st.success("✅ **Resolved:** Policy automatically updated to enforce AES-256 Tokenization.")
        else:
            # Behavioral Alert
            behavioral_found = False
            for f in state['findings']:
                if "BEHAVIORAL" in f or "High-Velocity" in f:
                    st.warning(f"**{f}**", icon="⚡")
                    behavioral_found = True
            
            # Policy Gaps
            for gap in state.get('policy_gaps', []):
                if "ESTIMATED LIABILITY" not in gap:
                    st.warning(f"**Violation:** {gap}", icon="⚠️")
            
            if not behavioral_found and not state.get('policy_gaps'):
                st.success("No Strategic Gaps Detected.", icon="✅")

    with col_chat:
        st.markdown("### 💬 AEGIS ASSISTANT")
        
        # Chat Container
        chat_container = st.container(height=380)
        
        # Chat Input
        user_query = st.chat_input("Query Agent Swarm...")
        
        if user_query:
            response = "**Aegis:** Based on the **High-Velocity AML Alert**, I recommend enabling **Rate Limiting (10 req/sec)** on the API gateway and implementing **Column-Level Encryption (CLE)**."
            st.session_state.history.append(("user", user_query))
            st.session_state.history.append(("ai", response))
        
        with chat_container:
            for role, msg in st.session_state.history:
                if role == "user":
                    st.markdown(f'<div class="user-msg">👤 <b>You:</b> {msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="ai-msg">🤖 <b>Aegis:</b> {msg}</div>', unsafe_allow_html=True)

        # ACTION BUTTON
        st.markdown("---")
        if not remediated and current_risk_val > 50:
            if st.button("⚡ EXECUTE AUTO-REMEDIATION", type="secondary", use_container_width=True):
                st.session_state.remediation_status = "COMPLETED"
                # Add to Audit Log
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.audit_log.append({"time": timestamp, "action": "Policy Patch: Tokenization + Rate Limiting"})
                st.rerun()

        # Download Report
        report_text = f"AEGIS STRATEGIC BRIEF\nDate: {datetime.now()}\nLiability Exposure: {fine_val}\nStatus: {status_text}\nFindings: {len(state['findings'])}"
        st.download_button("📥 DOWNLOAD BRIEF", report_text, "Aegis_Brief.txt", use_container_width=True)