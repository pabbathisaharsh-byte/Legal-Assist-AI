# ⚖️ LegalAssist AI
### Intelligent Multi-Agent Legal Document & Compliance Assistant

LegalAssist AI is an enterprise-grade **Agentic AI** application that assists legal professionals in analyzing contracts, reviewing compliance, conducting legal research, and drafting legal documents. The system uses a **Supervisor-based Multi-Agent Architecture** built with **LangGraph** and **LangChain** to intelligently coordinate specialized AI agents while maintaining conversation memory and validating responses through a Reflection Node. :contentReference[oaicite:0]{index=0}

---

## 🚀 Features

- 📄 Upload legal documents (PDF, DOCX, TXT)
- 📑 Contract clause extraction and summarization
- ✅ Compliance review against organizational policies
- 🔍 Legal research assistance
- 📝 Legal document drafting
- 🧠 Shared conversation memory
- 🤖 Supervisor Agent for intelligent routing
- 🔄 Reflection Node for response validation
- 💬 Interactive Streamlit chat interface

---

## 🏗️ System Architecture

```
                    User
                      │
              Streamlit Interface
                      │
              Supervisor Agent
                      │
        ┌─────────────┼─────────────┐
        │             │             │
 Contract        Compliance     Legal Research
 Analysis          Review            Agent
    │                 │
    └─────────────┬───┘
                  │
        Document Drafting Agent
                  │
        Shared Conversation Memory
                  │
           Reflection Node
                  │
            Final AI Response
```

---

## 🤖 AI Agents

### 1. Supervisor Agent
- Detects user intent
- Selects appropriate AI agents
- Coordinates workflow

### 2. Contract Analysis Agent
- Extracts important clauses
- Generates contract summaries

### 3. Compliance Review Agent
- Reviews uploaded contracts
- Identifies compliance issues

### 4. Legal Research Agent
- Answers legal questions
- Retrieves legal references

### 5. Document Drafting Agent
- Drafts legal documents
- Generates notices and agreements

### 6. Reflection Node
- Reviews outputs
- Improves consistency and completeness before presenting the final response

---

## 📂 Project Structure

```
LegalAssistAI/
│
├── agents/
│   ├── contract_analysis_agent.py
│   ├── compliance_review_agent.py
│   ├── legal_research_agent.py
│   ├── document_drafting_agent.py
│   └── reflection_node.py
│
├── memory/
│   ├── conversation_memory.py
│   └── state.py
│
├── prompts/
│
├── tools/
│   ├── clause_extractor.py
│   ├── compliance_checker.py
│   ├── document_parser.py
│   ├── legal_knowledge_base.py
│   └── template_generator.py
│
├── utils/
│
├── data/
│
├── app.py
├── graph.py
├── supervisor.py
├── requirements.txt
├── dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🛠️ Technologies Used

- Python 3.11+
- LangChain
- LangGraph
- Ollama (Llama 3.2)
- Streamlit
- ChromaDB
- Pydantic
- Pandas
- Matplotlib
- PyPDF
- Python-docx

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/your-username/LegalAssistAI.git

cd LegalAssistAI
```

### Create a virtual environment

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🦙 Install Ollama

Download and install Ollama

https://ollama.com

Pull the required model

```bash
ollama pull llama3.2
```

Run Ollama

```bash
ollama serve
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Open your browser

```
http://localhost:8501
```

---

## 📋 How It Works

1. Upload a legal document.
2. Ask questions about the document.
3. Supervisor Agent identifies the intent.
4. Required AI agents execute in parallel.
5. Shared memory maintains conversation context.
6. Reflection Node validates outputs.
7. Final response is displayed in Streamlit.

---

## 📷 Supported File Formats

- PDF
- DOCX
- TXT

---

## 📦 Python Dependencies

Major packages include:

```
langchain
langgraph
langchain-ollama
streamlit
pandas
chromadb
langchain-community
langchain-text-splitters
python-docx
pypdf
matplotlib
```

---

## 🎯 Future Enhancements

- OCR support for scanned documents
- Clause risk scoring
- RAG-based legal knowledge retrieval
- Contract comparison
- Compliance analytics dashboard
- Enterprise authentication
- Cloud deployment
- Multilingual legal support

---

## 📖 Learning Outcomes

This project demonstrates:

- Multi-Agent AI
- LangGraph Workflows
- Agent Orchestration
- Tool Calling
- Shared Memory
- Reflection-Based AI
- Prompt Engineering
- Streamlit Application Development

---

## ⚠️ Disclaimer

LegalAssist AI is intended to assist legal professionals by automating repetitive legal tasks. It does **not** provide legally binding advice or replace qualified legal experts.

---

## 👨‍💻 Developed By

Team E

Enterprise Agentic AI Capstone Project

---

## 📄 License

This project is developed for educational and research purposes.
