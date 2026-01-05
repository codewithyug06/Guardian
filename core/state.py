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
    
    # --- PHASE 9: TRUST & ROBUSTNESS (Previous Update) ---
    consensus_audit: Annotated[List[str], operator.add] 
    compliance_drift: float 
    audio_bytes: Any 
    jurisdiction: str 
    
    # --- PHASE 10: EXTRAORDINARY FEATURES (NEW) ---
    digital_twin_metrics: str                  # 1. Mirror Node Results
    vendor_risks: Annotated[List[str], operator.add] # 2. Supply Chain Intel
    decision_hash: str                         # 3. Immutable Merkle Root
    policy_update_proposal: str                # 4. Auto-Legislator Draft
    adaptive_sensitivity: float                # 5. The Chameleon Metric