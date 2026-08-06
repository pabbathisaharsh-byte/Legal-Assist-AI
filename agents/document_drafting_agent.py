from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from memory.state import LegalAssistState
from utils.config import OLLAMA_HOST  
import os
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
llm = ChatOllama(model="llama3.2", temperature=0, base_url=OLLAMA_HOST)
class DraftDocument(BaseModel):
    document_type: str = Field(description="e.g. Termination Notice, NDA, Demand Letter")
    draft_content: str = Field(description="The full drafted document text")
    notes: str = Field(description="Any assumptions made or placeholders the user should fill in")

llm = ChatOllama(model="llama3.2", temperature=0.3)  # slightly higher temp — drafting benefits from some flexibility
structured_llm = llm.with_structured_output(DraftDocument)

DRAFTING_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Document Drafting Agent for a legal assistant platform.
Draft professional, clearly structured legal correspondence or document sections based on
the user's instructions. Use standard legal document formatting and placeholders like
[PARTY NAME] or [DATE] where specific details are not provided.
This is a DRAFT for review by a qualified legal professional — it is not final legal advice."""),
    ("human", """User Instructions: {user_request}

Relevant Context (if any):
Clause Summary: {clause_summary}
Compliance Findings: {compliance_report}""")
])

def document_drafting_agent(state: LegalAssistState) -> dict:
    chain = DRAFTING_PROMPT | structured_llm
    result: DraftDocument = chain.invoke({
        "user_request": state.get("user_request", ""),
        "clause_summary": state.get("clause_summary", "None"),
        "compliance_report": state.get("compliance_report", "None")
    })

    return {
        "drafted_document": result.model_dump()
    }