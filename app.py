import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
from core.graph import build_compliance_graph

# 1. Load Environment Variables
load_dotenv()

# --- PAGE CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="Sentinels | Agentic Compliance",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR "WORLD CLASS" UI ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    /* Custom Alert Boxes */
    .stAlert {
        border-radius: 8px;
        border: 1px solid #30363D;
    }
    
    /* Header Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Chat Bubbles */
    .user-msg {
        background-color: #262730;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        border-left: 3px solid #FF4B4B;
    }
    .ai-msg {
        background-color: #004E98;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 3px solid #00C2FF;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_logo, col_title = st.columns([1, 10])
with col_logo:
    st.markdown("## 🛡️") 
with col_title:
    st.title("Sentinels AI | Autonomous Compliance Guard")
    st.markdown("**Real-time. Agentic. Self-Healing. Predictive.**")

st.markdown("---")

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []
if "remediation_status" not in st.session_state:
    st.session_state.remediation_status = "PENDING"
if "audit_log" not in st.session_state:
    st.session_state.audit_log = [] # Store historical actions

# --- SIDEBAR DASHBOARD ---
with st.sidebar:
    st.markdown("### 📡 System Status")
    
    # API Key Check
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.warning("⚠️ **Circuit Breaker Mode**\n(Simulation Active)")
    else:
        st.success("✅ **Core Systems Online**")

    st.markdown("---")
    st.markdown("### 🤖 Agent Swarm")
    
    # Status Indicators with styled markdown
    st.markdown("🟢 **Scout** _(Scanning)_")
    st.markdown("🟢 **Sentry** _(Monitoring)_")
    st.markdown("🟢 **Architect** _(Planning)_")
    st.markdown("🟢 **Prophet** _(Forecasting)_") # NEW AGENT ROLE
    
    # Dynamic Visa Guard Status
    if "final_state" in st.session_state:
        if st.session_state.remediation_status == "COMPLETED":
             st.markdown("🟢 **Visa Guard** _(Secure)_")
        elif st.session_state.final_state.get('risk_level') in ["HIGH", "CRITICAL"]:
            st.markdown("🔴 **Visa Guard** _(ENFORCING)_")
    else:
        st.markdown("🟡 **Visa Guard** _(Standby)_")

    st.markdown("---")
    
    # NEW: Recent Audit Logs Sidebar
    st.markdown("### 🕒 Recent Actions")
    if st.session_state.audit_log:
        for log in reversed(st.session_state.audit_log[-3:]): # Show last 3
            st.caption(f"**{log['time']}**: {log['action']}")
    else:
        st.caption("No remediation actions yet.")

    st.markdown("---")
    st.info("ℹ️ **Version 3.0.0** (Predictive Build)")

# --- MAIN CONTROLS ---
col_action1, col_action2, col_spacer = st.columns([2, 2, 4])
with col_action1:
    run_btn = st.button("🚀 Initialize Audit Cycle", type="primary", use_container_width=True)

if run_btn:
    st.session_state.remediation_status = "PENDING"
    engine = build_compliance_graph()
    
    # Improved Spinner UX
    with st.spinner("🤖 Agents orchestrating compliance review & predictive analysis..."):
        # Invoke Graph
        final_state = engine.invoke({"findings": [], "risk_level": "UNKNOWN", "policy_gaps": []})
        st.session_state.final_state = final_state 
        st.toast("✅ Audit Cycle Complete!", icon="🛡️")

# --- DASHBOARD LAYOUT ---
if "final_state" in st.session_state:
    state = st.session_state.final_state
    remediated = st.session_state.remediation_status == "COMPLETED"

    # 1. DYNAMIC BANNER
    if remediated:
        st.success("##### ✅ SYSTEM SECURED: Policy Updated & Visa Gateway Unblocked.")
        current_risk_val = 0
    else:
        visa_alert = next((f for f in reversed(state['findings']) if "VISA GATEWAY" in f), None)
        if visa_alert and "BLOCKED" in visa_alert:
            st.error(f"##### ⛔ {visa_alert}")
        elif visa_alert:
            st.success(f"##### ✅ {visa_alert}")
        
        current_risk_val = 99 if state.get('risk_level') in ["HIGH", "CRITICAL"] else 15

    # 2. METRICS ROW
    col1, col2, col3 = st.columns(3)
    with col1:
        delta_color = "normal" if remediated else ("inverse" if current_risk_val > 50 else "normal")
        st.metric("Systemic Risk Index", f"{current_risk_val}%", 
                  "-99%" if remediated else ("-12%" if current_risk_val > 50 else "+5%"),
                  delta_color=delta_color)
    with col2:
        st.metric("Active Agents", "4", "All Systems Go")
    with col3:
        status_text = "SECURE" if remediated else ("CRITICAL" if current_risk_val > 50 else "STABLE")
        st.metric("Compliance Posture", status_text, "Policy v2.2" if remediated else "Policy v2.1")

    # 3. DETAILED VIEW (Split Layout)
    col_viz, col_chat = st.columns([1.3, 1])

    with col_viz:
        # --- NEW: PREDICTIVE FORECAST CHART ---
        st.subheader("📈 Risk Forecast (30 Days)")
        
        # Simulate Predictive Data
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        if remediated:
            # Flatline at 0 if fixed
            risk_trend = [random.randint(0, 5) for _ in range(30)]
        else:
            # Rising trend if not fixed
            risk_trend = [min(100, x * 3 + random.randint(-5, 5)) for x in range(30)]
        
        trend_df = pd.DataFrame({"Date": dates, "Projected Risk": risk_trend})
        
        fig_trend = px.area(trend_df, x="Date", y="Projected Risk", 
                            color_discrete_sequence=['#FF4B4B' if not remediated else '#00C2FF'])
        fig_trend.update_layout(height=250, margin=dict(l=20, r=20, t=10, b=20),
                                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_trend, use_container_width=True)

        # Policy Gap Cards
        st.subheader("⚠️ Detected Gaps")
        if remediated:
            st.success("✅ **Resolved:** Policy automatically updated to enforce AES-256 Tokenization.")
        elif state.get('policy_gaps'):
            for gap in state['policy_gaps']:
                st.warning(f"**Violation Detected:**\n\n{gap}", icon="⚠️")
        else:
            st.success("No Policy Gaps Detected.", icon="✅")

    with col_chat:
        st.subheader("💬 Compliance Assistant")
        
        # Chat History Container
        chat_container = st.container(height=350)
        
        # Input Area
        user_query = st.chat_input("Ask about remediation (e.g., 'How do I fix this?')")
        
        if user_query:
            response = (
                "**Agent Recommendation:** Based on the PCI-DSS 3.4 violation, "
                "I recommend implementing **Column-Level Encryption (CLE)** using AES-256. "
                "I can generate a Terraform script for this."
            )
            st.session_state.history.append(("user", user_query))
            st.session_state.history.append(("ai", response))
        
        # Render Chat
        with chat_container:
            for role, msg in st.session_state.history:
                if role == "user":
                    st.markdown(f'<div class="user-msg">👤 <b>You:</b> {msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="ai-msg">🤖 <b>Agent:</b> {msg}</div>', unsafe_allow_html=True)

        # 4. ACTION & REPORTING SECTION
        st.markdown("### 🛠️ Remediation & Reports")
        
        if not remediated and current_risk_val > 50:
            if st.button("⚡ Execute Auto-Remediation", type="primary", use_container_width=True):
                # Update State
                st.session_state.remediation_status = "COMPLETED"
                # Add to Audit Log
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.audit_log.append({"time": timestamp, "action": "Applied Policy Fix: AES-256"})
                st.rerun()
        
        # Report Generator
        report_text = f"AUDIT REPORT\nDate: {datetime.now()}\nStatus: {status_text}\nFindings: {len(state['findings'])}"
        st.download_button(
            label="📥 Download Evidence Package",
            data=report_text,
            file_name="Audit_Evidence.txt",
            mime="text/plain",
            use_container_width=True
        )