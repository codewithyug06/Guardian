from typing import TypedDict, List, Annotated, Any
import operator

class AgentState(TypedDict):
    # --- BASE FIELDS (Existing) ---
    findings: Annotated[List[str], operator.add] 
    risk_level: str
    remediation_plan: str
    evidence_package: str
    policy_gaps: Annotated[List[str], operator.add]
    
    # --- PHASE 1: REFLECTION ---
    scout_retries: int
    scout_confidence: str
    
    # --- PHASE 2: GEN AI ---
    generated_code: str
    
    # --- PHASE 3: PREDICTIVE ML ---
    risk_forecast: List[int] 
    
    # --- PHASE 4: MULTI-MODAL (VISION) ---
    uploaded_image_bytes: Any
    
    # --- PHASE 5: ADVERSARIAL ---
    red_team_mode: bool
    
    # --- PHASE 8: FEDERATED LEARNING ---
    federated_mode: bool 
    federated_logs: Annotated[List[str], operator.add] 
    
    # --- FINAL WINNING ADVANCEMENTS (NEW) ---
    consensus_audit: Annotated[List[str], operator.add] # Stores cross-agent validation logs
    compliance_drift: float # 0-100% Score for CFO Dashboard
    audio_bytes: Any # For Audio Sentry
    jurisdiction: str # EU/US/APAC mode