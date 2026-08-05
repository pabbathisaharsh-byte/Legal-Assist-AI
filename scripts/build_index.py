# scripts/build_index.py

"""
One-time setup script: builds and persists the Chroma vector store
from the reference documents in data/legal_knowledge/.

Run this ONCE before starting the Streamlit app (and again any time
you add/change files in data/legal_knowledge/).

Usage:
    python scripts/build_index.py
"""

import sys
import os

# allow running from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.legal_knowledge_base import build_vector_store

if __name__ == "__main__":
    print("Building legal knowledge base vector store...")
    build_vector_store()
    print("Done. Vector store persisted to data/chroma_store/")