from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    # 'Annotated' allows agents to append findings without overwriting each other
    findings: Annotated[List[str], operator.add] 
    risk_level: str
    remediation_plan: str
    evidence_package: str
    # Specific list of gaps found between Regs vs. Policy
    policy_gaps: Annotated[List[str], operator.add]