from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import AgentState
from .agents import scout_agent, sentry_agent, architect_agent, visa_enforcement_agent, coder_agent

def should_scout_continue(state: AgentState):
    """
    Decides if Scout needs to loop back (Self-Correction) 
    or move forward to Sentry.
    """
    if state.get("scout_confidence") == "Low" and state.get("scout_retries", 0) < 3:
        return "retry"
    return "continue"

def build_compliance_graph():
    workflow = StateGraph(AgentState)
    
    # 1. Initialize Memory
    memory = MemorySaver()

    # 2. Define Nodes
    workflow.add_node("scout", scout_agent)
    workflow.add_node("sentry", sentry_agent)
    workflow.add_node("architect", architect_agent)
    workflow.add_node("coder", coder_agent)  # Phase 2 Node
    workflow.add_node("visa_guard", visa_enforcement_agent)

    # 3. Define Flow
    workflow.set_entry_point("scout")
    
    workflow.add_conditional_edges(
        "scout",
        should_scout_continue,
        {
            "retry": "scout",
            "continue": "sentry"
        }
    )
    
    workflow.add_edge("sentry", "architect")
    workflow.add_edge("architect", "coder") # Architect -> Coder
    workflow.add_edge("coder", "visa_guard") # Coder -> Enforcement
    workflow.add_edge("visa_guard", END)

    # 4. Compile with Interrupts & Memory
    return workflow.compile(checkpointer=memory, interrupt_before=["visa_guard"])