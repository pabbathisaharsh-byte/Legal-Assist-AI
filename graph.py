# graph.py

from langgraph.graph import StateGraph, END
from memory.state import LegalAssistState
from supervisor import route_request, VALID_AGENTS
from agents.contract_analysis_agent import contract_analysis_agent
from agents.compliance_review_agent import compliance_review_agent
from agents.legal_research_agent import legal_research_agent
from agents.document_drafting_agent import document_drafting_agent
from agents.reflection_node import reflection_node
from memory.conversation_memory import get_checkpointer

def route_to_agents(state: LegalAssistState) -> list:
    """
    Conditional edge function: reads next_agents (set by Supervisor)
    and returns the list of node names to fan out to.
    LangGraph runs all returned nodes, then converges before the next node.
    """
    return state.get("next_agents", []) or ["legal_research_agent"]


def build_graph():
    graph = StateGraph(LegalAssistState)

    # Nodes
    graph.add_node("supervisor", route_request)
    graph.add_node("contract_analysis_agent", contract_analysis_agent)
    graph.add_node("compliance_review_agent", compliance_review_agent)
    graph.add_node("legal_research_agent", legal_research_agent)
    graph.add_node("document_drafting_agent", document_drafting_agent)
    graph.add_node("reflection", reflection_node)

    # Entry point
    graph.set_entry_point("supervisor")

    # Fan-out: supervisor -> one or more agent nodes
    graph.add_conditional_edges(
        "supervisor",
        route_to_agents,
        VALID_AGENTS  # tells LangGraph the possible destination node names
    )

    # Fan-in: every agent node converges into reflection
    for agent_name in VALID_AGENTS:
        graph.add_edge(agent_name, "reflection")
    graph.add_edge("reflection", END)
    checkpointer = get_checkpointer()
    return graph.compile(checkpointer=checkpointer)