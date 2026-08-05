import streamlit as st
import uuid
from graph import build_graph
from tools.document_parser import parse_document

st.set_page_config(page_title="LegalAssist AI", layout="wide")
st.title("LegalAssist AI")
st.caption("Multi-Agent Legal Document & Compliance Assistant — AI-assisted, not a substitute for legal advice.")

# ---- Session setup ----
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {"role": ..., "content": ...} for display

if "document_text" not in st.session_state:
    st.session_state.document_text = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

@st.cache_resource
def get_compiled_graph():
    return build_graph()

compiled_graph = get_compiled_graph()
with st.sidebar:
    st.header("Upload Contract")
    uploaded_file = st.file_uploader("Upload a contract (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

    if uploaded_file is not None and uploaded_file.name != st.session_state.document_name:
        with st.spinner("Parsing document..."):
            text = parse_document(uploaded_file)
            st.session_state.document_text = text
            st.session_state.document_name = uploaded_file.name
        st.success(f"Loaded: {uploaded_file.name}")

    if st.session_state.document_name:
        st.info(f"Active document: **{st.session_state.document_name}**")
        if st.button("Clear document"):
            st.session_state.document_text = None
            st.session_state.document_name = None
            st.rerun()

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about your contract, compliance, legal research, or request a draft...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    graph_input = {
        "user_request": user_input,
        "document_text": st.session_state.document_text,
        "document_name": st.session_state.document_name,
    }

    with st.chat_message("assistant"):
        with st.spinner("Coordinating agents..."):
            result = compiled_graph.invoke(graph_input, config=config)

        final_response = result.get("final_response", "Sorry, I couldn't generate a response.")
        st.markdown(final_response)

        with st.expander("Agent details"):
            st.write("**Intent detected:**", result.get("intent"))
            st.write("**Agents invoked:**", result.get("next_agents"))
            if result.get("clause_summary"):
                st.write("**Clause Summary:**", result.get("clause_summary"))
            if result.get("compliance_report"):
                st.write("**Compliance Report:**", result.get("compliance_report"))
            if result.get("research_summary"):
                st.write("**Research Summary:**", result.get("research_summary"))
            if result.get("drafted_document"):
                st.write("**Drafted Document:**", result.get("drafted_document"))
            st.write("**Reflection notes:**", result.get("reflection_notes"))
            st.write("**Approved:**", result.get("is_response_approved"))

    st.session_state.chat_history.append({"role": "assistant", "content": final_response})