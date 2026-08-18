from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from .state import AgentState
from .agents import (
    scout_agent, sentry_agent, architect_agent, 
    visa_enforcement_agent, coder_agent, prophet_agent, 
    ghost_agent, federated_agent, consensus_agent, mirror_agent
)

# Initialize global SQLite connection for persistence
_conn = sqlite3.connect("guardian_state.sqlite", check_same_thread=False)
_memory = SqliteSaver(_conn)
_memory.setup()

def should_scout_continue(state: AgentState):
    if state.get("scout_confidence") == "Low" and state.get("scout_retries", 0) < 3:
        return "retry"
    return "continue"

def should_mirror_continue(state: AgentState):
    report = state.get("digital_twin_metrics", "")
    retries = state.get("coder_retries", 0)
    if "FAIL" in report and retries < 2:
        return "retry"
    return "continue"

def build_compliance_graph():
    workflow = StateGraph(AgentState)
    memory = _memory

    # Define Nodes
    workflow.add_node("scout", scout_agent)
    workflow.add_node("ghost", ghost_agent)
    workflow.add_node("federated", federated_agent)
    workflow.add_node("sentry", sentry_agent)
    workflow.add_node("architect", architect_agent)
    workflow.add_node("coder", coder_agent)
    workflow.add_node("mirror", mirror_agent) # NEW NODE
    workflow.add_node("consensus", consensus_agent)
    workflow.add_node("prophet", prophet_agent)
    workflow.add_node("visa_guard", visa_enforcement_agent)

    # Define Flow
    workflow.set_entry_point("scout")
    
    workflow.add_conditional_edges(
        "scout",
        should_scout_continue,
        {
            "retry": "scout",
            "continue": "ghost"
        }
    )
    
    workflow.add_edge("ghost", "federated") 
    workflow.add_edge("federated", "sentry") 
    workflow.add_edge("sentry", "architect")
    workflow.add_edge("architect", "coder")
    workflow.add_edge("coder", "mirror") # Coder -> Mirror
    workflow.add_conditional_edges(
        "mirror",
        should_mirror_continue,
        {
            "retry": "coder",
            "continue": "consensus"
        }
    )
    workflow.add_edge("consensus", "prophet") 
    workflow.add_edge("prophet", "visa_guard")
    workflow.add_edge("visa_guard", END)

    return workflow.compile(checkpointer=memory, interrupt_before=["visa_guard"])