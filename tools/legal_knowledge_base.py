# tools/legal_knowledge_base.py

import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from utils.config import OLLAMA_HOST  
KNOWLEDGE_DIR = os.path.join("data", "legal_knowledge")
PERSIST_DIR = os.path.join("data", "chroma_store")

embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_HOST)

def build_vector_store():
    """
    Run this ONCE (setup script) to build/persist the vector index
    from the reference documents in data/legal_knowledge/.
    """
    loader = DirectoryLoader(KNOWLEDGE_DIR, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    print(f"Indexed {len(chunks)} chunks from {len(docs)} documents.")
    return vector_store

def get_vector_store():
    """
    Load the already-persisted vector store (used at query time by the agent).
    """
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

def search_legal_knowledge(query: str, k: int = 3) -> list:
    """
    Retrieval function the Legal Research Agent calls.
    Returns top-k relevant chunks as list of dicts.
    """
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return [{"content": r.page_content, "source": r.metadata.get("source", "unknown")} for r in results]