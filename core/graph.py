from langgraph.graph import StateGraph, END
from .state import AgentState
from .agents import scout_agent, sentry_agent, architect_agent, visa_enforcement_agent

def build_compliance_graph():
    workflow = StateGraph(AgentState)

    # Define Nodes
    workflow.add_node("scout", scout_agent)
    workflow.add_node("sentry", sentry_agent)
    workflow.add_node("architect", architect_agent)
    workflow.add_node("visa_guard", visa_enforcement_agent)

    # Set Workflow Path: Scout -> Sentry -> Architect -> Visa Guard
    workflow.set_entry_point("scout")
    workflow.add_edge("scout", "sentry")
    workflow.add_edge("sentry", "architect")
    workflow.add_edge("architect", "visa_guard")
    workflow.add_edge("visa_guard", END)

    return workflow.compile()