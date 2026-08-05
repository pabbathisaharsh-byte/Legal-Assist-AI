# supervisor.py

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from memory.state import LegalAssistState
from utils.config import OLLAMA_HOST
VALID_AGENTS = [
    "contract_analysis_agent",
    "compliance_review_agent",
    "legal_research_agent",
    "document_drafting_agent"
]

class RoutingDecision(BaseModel):
    intent: str = Field(description="Short label for what the user wants")
    next_agents: List[str] = Field(
        description=f"Which agents to invoke. Must be a subset of: {VALID_AGENTS}"
    )
    reasoning: str = Field(description="Brief reason for this routing decision")

llm = ChatOllama(model="llama3.2", temperature=0, base_url=OLLAMA_HOST)
structured_llm = llm.with_structured_output(RoutingDecision)

SUPERVISOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", f"""You are the Supervisor Agent for a legal assistant platform.
Given a user's request, decide which specialized agent(s) should handle it.

Available agents:
- contract_analysis_agent: extracts and summarizes clauses from an uploaded contract
- compliance_review_agent: checks an uploaded contract against organizational compliance policies
- legal_research_agent: answers legal questions using a legal knowledge base
- document_drafting_agent: drafts legal documents, notices, or letters

Rules:
- Only select agents that are actually relevant to the request.
- A request to "review this contract for compliance" should select BOTH
  contract_analysis_agent and compliance_review_agent.
- A request that is purely a legal question with no document should select
  only legal_research_agent.
- A request to draft/write something should include document_drafting_agent.
- next_agents must only contain values from: {VALID_AGENTS}"""),
    ("human", "User request: {user_request}\n\nDocument uploaded: {has_document}")
])

def route_request(state: LegalAssistState) -> dict:
    chain = SUPERVISOR_PROMPT | structured_llm
    result: RoutingDecision = chain.invoke({
        "user_request": state.get("user_request", ""),
        "has_document": bool(state.get("document_text"))
    })

    valid_next_agents = [a for a in result.next_agents if a in VALID_AGENTS]

    # Deterministic safety net: document-dependent agents are useless
    # without an uploaded document, regardless of what the LLM picked.
    has_document = bool(state.get("document_text"))
    if not has_document:
        document_dependent = {"contract_analysis_agent", "compliance_review_agent"}
        valid_next_agents = [a for a in valid_next_agents if a not in document_dependent]

    if not valid_next_agents:
        valid_next_agents = ["legal_research_agent"]

    return {
        "intent": result.intent,
        "next_agents": valid_next_agents,
        "clause_summary": None,
        "compliance_report": None,
        "research_summary": None,
        "drafted_document": None,
    }