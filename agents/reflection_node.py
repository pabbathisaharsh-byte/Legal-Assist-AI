# agents/reflection_node.py

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from memory.state import LegalAssistState
from utils.config import OLLAMA_HOST  
class ReflectionResult(BaseModel):
    is_approved: bool
    notes: str = Field(description="What was checked, and any gaps or issues found")
    final_response: str = Field(description="The polished final response to show the user")

llm = ChatOllama(model="llama3.2", temperature=0, base_url=OLLAMA_HOST)
structured_llm = llm.with_structured_output(ReflectionResult)

REFLECTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the Reflection Node for a legal assistant platform.
Review the outputs produced by the specialized agents for completeness, consistency,
and clarity. Then compose a single, well-structured final response for the user that
combines the relevant agent outputs. Do not invent information not present in the
agent outputs. Always include a brief disclaimer that this is AI-assisted output,
not a substitute for qualified legal advice.

For 'notes': write 2-3 full sentences explaining specifically what you checked and
why you approved or did not approve the response. Never respond with just a title
or label — always explain your reasoning."""),
    ("human", """User Request: {user_request}

Clause Summary: {clause_summary}
Compliance Report: {compliance_report}
Research Summary: {research_summary}
Drafted Document: {drafted_document}""")
])

def reflection_node(state: LegalAssistState) -> dict:
    chain = REFLECTION_PROMPT | structured_llm
    result: ReflectionResult = chain.invoke({
        "user_request": state.get("user_request", ""),
        "clause_summary": state.get("clause_summary", "Not generated"),
        "compliance_report": state.get("compliance_report", "Not generated"),
        "research_summary": state.get("research_summary", "Not generated"),
        "drafted_document": state.get("drafted_document", "Not generated")
    })

    return {
        "is_response_approved": result.is_approved,
        "reflection_notes": result.notes,
        "final_response": result.final_response
    }