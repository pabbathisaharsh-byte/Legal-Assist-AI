from typing import TypedDict, Optional, List, Dict, Any, Annotated
from langgraph.graph.message import add_messages


class LegalAssistState(TypedDict):
    # Conversation
    messages: Annotated[List[Dict], add_messages]   # chat history (LangGraph handles append)
    user_request: str                                 # current raw user input

    # Routing (Supervisor's decision)
    intent: Optional[str]                              # e.g. "contract_analysis", "compliance_review"
    next_agents: List[str]                              # which agents to invoke, in order

    # Document context
    document_text: Optional[str]                        # parsed text of uploaded contract
    document_name: Optional[str]

    # Agent outputs
    clause_summary: Optional[Dict[str, Any]]             # Contract Analysis Agent output
    compliance_report: Optional[Dict[str, Any]]          # Compliance Review Agent output
    research_summary: Optional[Dict[str, Any]]           # Legal Research Agent output
    drafted_document: Optional[Dict[str, Any]]           # Document Drafting Agent output

    # Reflection
    reflection_notes: Optional[str]
    is_response_approved: bool

    # Final output
    final_response: Optional[str]