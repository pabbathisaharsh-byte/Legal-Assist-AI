from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from memory.state import LegalAssistState
from tools.compliance_checker import load_policies, keyword_precheck

import os
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

llm = ChatOllama(model="llama3.2", temperature=0, base_url=OLLAMA_HOST)

class ComplianceFinding(BaseModel):
    policy_id: str
    category: str
    status: str = Field(description="One of: Compliant, Non-Compliant, Partially Compliant")
    explanation: str

class ComplianceReport(BaseModel):
    findings: List[ComplianceFinding]
    overall_status: str = Field(description="One of: Compliant, Non-Compliant, Needs Review")
    missing_requirements: List[str]

llm = ChatOllama(model="llama3.2", temperature=0)
structured_llm = llm.with_structured_output(ComplianceReport)

COMPLIANCE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Compliance Review Agent for a legal assistant platform.
You are given a contract and a keyword pre-check against organizational policies.
For each policy, determine if the contract is Compliant, Non-Compliant, or Partially Compliant,
based on the actual contract text — not just keyword presence. Explain your reasoning briefly.
Do not provide legal advice — only compliance assessment against the given policies."""),
    ("human", """Contract Text:
{document_text}

Policies to check (with keyword pre-check results):
{policy_precheck}""")
]) 

def compliance_review_agent(state: LegalAssistState) -> dict:
    document_text = state.get("document_text", "")

    if not document_text:
        return {"compliance_report": {"error": "No document text found in state."}}

    policies = load_policies()
    precheck = keyword_precheck(document_text, policies)

    chain = COMPLIANCE_PROMPT | structured_llm
    result: ComplianceReport = chain.invoke({
        "document_text": document_text,
        "policy_precheck": precheck
    })

    return {
        "compliance_report": result.model_dump()
    }