from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from memory.state import LegalAssistState
from tools.legal_knowledge_base import search_legal_knowledge

import os
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
llm = ChatOllama(model="llama3.2", temperature=0, base_url=OLLAMA_HOST)
class ResearchSummary(BaseModel):
    query_topic: str
    relevant_references: List[str] = Field(description="Key points found from legal knowledge base")
    summary: str = Field(description="Synthesized summary answering the user's legal research question")
    sources: List[str] = Field(description="Source document names referenced")

llm = ChatOllama(model="llama3.2", temperature=0)
structured_llm = llm.with_structured_output(ResearchSummary)

RESEARCH_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Legal Research Agent. You are given retrieved reference material
and a user's legal question. Synthesize a clear, accurate summary based ONLY on the retrieved
content. If the retrieved content doesn't fully answer the question, say so explicitly.
Do not provide legal advice — only research synthesis."""),
    ("human", """User Question: {user_request}

Retrieved Reference Material:
{retrieved_content}""")
])

def legal_research_agent(state: LegalAssistState) -> dict:
    query = state.get("user_request", "")

    retrieved = search_legal_knowledge(query, k=3)
    retrieved_text = "\n\n".join(
        f"[Source: {r['source']}]\n{r['content']}" for r in retrieved
    )

    chain = RESEARCH_PROMPT | structured_llm
    result: ResearchSummary = chain.invoke({
        "user_request": query,
        "retrieved_content": retrieved_text
    })

    return {
        "research_summary": result.model_dump()
    }