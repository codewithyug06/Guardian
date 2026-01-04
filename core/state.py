from typing import TypedDict, List, Annotated, Any
import operator

class AgentState(TypedDict):
    # 'Annotated' allows agents to append findings without overwriting each other
    findings: Annotated[List[str], operator.add] 
    risk_level: str
    remediation_plan: str
    evidence_package: str
    # Specific list of gaps found between Regs vs. Policy
    policy_gaps: Annotated[List[str], operator.add]
    
    # --- PHASE 1: REFLECTION ---
    scout_retries: int
    scout_confidence: str
    
    # --- PHASE 2: GEN AI ---
    generated_code: str
    
    # --- PHASE 3: PREDICTIVE ML ---
    # Stores the 30-day risk trend [val1, val2, ...]
    risk_forecast: List[int]