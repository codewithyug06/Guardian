from typing import TypedDict, List, Annotated, Any
import operator

class AgentState(TypedDict):
    # Base Fields
    findings: Annotated[List[str], operator.add] 
    risk_level: str
    remediation_plan: str
    evidence_package: str
    policy_gaps: Annotated[List[str], operator.add]
    
    # Phase 1: Reflection
    scout_retries: int
    scout_confidence: str
    
    # Phase 2: GenAI Patching
    generated_code: str
    
    # Phase 3: Predictive ML
    risk_forecast: List[int] 
    
    # Phase 4: Multi-Modal
    uploaded_image_bytes: Any
    
    # Phase 5: Adversarial
    red_team_mode: bool
    
    # --- PHASE 8: FEDERATED LEARNING (NEW) ---
    federated_mode: bool # True if connected to Privacy Net
    federated_logs: Annotated[List[str], operator.add] # Shared Intel Logs