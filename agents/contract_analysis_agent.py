from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from memory.state import LegalAssistState
from utils.config import OLLAMA_HOST  
import os
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
llm = ChatOllama(model="llama3.2", temperature=0, base_url=OLLAMA_HOST)
# ---- Structured output schema ----
class ClauseSummary(BaseModel):
    parties_involved: List[str] = Field(description="Names of parties in the contract")
    key_clauses: List[str] = Field(description="Important clauses found, e.g. termination, payment, liability")
    obligations: List[str] = Field(description="Key obligations of each party")
    risk_flags: List[str] = Field(description="Potentially risky or unusual clauses worth flagging")
    summary: str = Field(description="A concise plain-language summary of the contract")

# ---- LLM setup ----
llm = ChatOllama(model="llama3.2", temperature=0)
structured_llm = llm.with_structured_output(ClauseSummary)

CONTRACT_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Contract Analysis Agent for a legal assistant platform.
Analyze the given contract text and extract structured information.
Be precise and only extract what is explicitly present in the document.
Do not provide legal advice — only factual extraction and summarization."""),
    ("human", "Contract Text:\n\n{document_text}")
])

def contract_analysis_agent(state: LegalAssistState) -> dict:
    """
    Reads document_text from state, extracts clauses, returns updated field.
    """
    document_text = state.get("document_text", "")

    if not document_text:
        return {
            "clause_summary": {
                "error": "No document text found in state. Please upload a contract first."
            }
        }

    chain = CONTRACT_ANALYSIS_PROMPT | structured_llm
    result: ClauseSummary = chain.invoke({"document_text": document_text})

    return {
        "clause_summary": result.model_dump()
    }