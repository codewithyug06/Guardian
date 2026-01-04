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
    risk_forecast: List[int] # Stores the 30-day prediction array
    
    # --- PHASE 4: MULTI-MODAL (NEW) ---
    uploaded_image_bytes: Any # Holds raw image data for Vision Sentry