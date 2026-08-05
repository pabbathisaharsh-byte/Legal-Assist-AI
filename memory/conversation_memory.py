# memory/conversation_memory.py

from langgraph.checkpoint.memory import MemorySaver

def get_checkpointer():
    """
    Returns an in-memory checkpointer. Persists conversation state
    (messages, document context, prior agent outputs) across turns
    within the same session, keyed by thread_id.

    Note: this is in-process memory only — it resets when the Streamlit
    app restarts. That's acceptable for this project's scope (a single
    demo session). For true persistence across app restarts, swap this
    for SqliteSaver (see note below).
    """
    return MemorySaver()