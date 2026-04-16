# AI-Powered Project Intelligence Assistant

An end-to-end multi-agent RAG system that ingests project documents and answers questions about project status, risks, and budgets.

## Live Demo
- Frontend: https://gamuda-sharen.vercel.app
- Backend: https://gamudasharen-backend.onrender.com
- API Docs: https://gamudasharen-backend.onrender.com/docs

## Overview
This project is a lightweight project intelligence assistant built for the Gamuda Technologies Junior AI Engineer take-home assessment. It supports document upload, retrieval-augmented question answering, and query routing between specialized agents.

The system is designed to handle realistic project documents such as:
- project status reports
- risk registers
- structured data files

## Features
- Upload PDF, CSV, and TXT documents
- Chunk, embed, and index uploaded files
- Multi-agent routing:
  - Document Q&A Agent
  - Data Analysis Agent
- Source-aware responses
- Conversation session support through `session_id`
- FastAPI backend with REST API
- React/Vite frontend deployed on Vercel
- ChromaDB vector store for retrieval

## Tech Stack

### Backend
- FastAPI
- LangChain
- Google Gemini
- ChromaDB

### Frontend
- React
- Vite
- Framer Motion
- Modern utility-class styling

### Deployment
- Render for backend
- Vercel for frontend

## Architecture Summary
The system follows a simple multi-agent RAG architecture:

1. User uploads a document
2. Backend ingests and chunks the document
3. Chunks are embedded and stored in ChromaDB
4. User submits a question
5. Router decides whether the query is:
   - document-oriented
   - data-oriented
6. Appropriate agent retrieves relevant chunks
7. LLM generates the final answer
8. Frontend displays answer, confidence, and sources

## Project Structure

```text
.
├── main.py
├── requirements.txt
├── ARCHITECTURE.md
├── DECISIONS.md
├── agents/
│   ├── __init__.py
│   ├── router.py
│   ├── doc_agent.py
│   └── data_agent.py
├── rag/
│   ├── __init__.py
│   ├── ingestor.py
│   └── retriever.py
└── my-ui/
    ├── src/
    ├── public/
    ├── package.json
    └── vite.config.js



    API Endpoints
GET /health → health check
POST /upload → upload and ingest a file
POST /chat → ask a question
Example Questions

Try prompts like:

What is the status of Project Gamma?
Summarize project_beta_status.pdf
What are the highest risks in the risk register?
Compare Alpha and Beta progress
What budget issues were reported?
Local Setup
1. Clone the repository
git clone https://github.com/sharen46/GamudaSharen.git
cd GamudaSharen
2. Backend setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
3. Frontend setup
cd my-ui
npm install
npm run dev
Environment Variables
Backend

Create a .env file or configure environment variables with:

GOOGLE_API_KEY=your_google_gemini_api_key
CHROMA_PATH=./chroma_db
Frontend

Set:

VITE_API_BASE_URL=https://gamudasharen-backend.onrender.com

For local development, this may point to your local backend instead.

Deployment Notes
Backend

The backend is deployed on Render.

Important settings:

Start command:

uvicorn main:app --host 0.0.0.0 --port $PORT
Python version pinned for compatibility
GOOGLE_API_KEY must be configured in Render
Frontend

The frontend is deployed on Vercel.

Important settings:

Root Directory: my-ui
Framework: Vite
Environment variable:
VITE_API_BASE_URL=https://gamudasharen-backend.onrender.com
Design Choices

This project intentionally prioritizes:

a working end-to-end system
simple and understandable architecture
modular code separation
fast deployment and demo readiness
clarity over unnecessary complexity
Known Limitations
Session handling is lightweight and not durable across restarts
ChromaDB uses local persistence for prototype simplicity
Vague prompts may still be routed to the wrong agent
Source references are returned at document level in the UI
Free-tier hosting may sleep and cause cold-start delays
Future Improvements
stronger rule-based + fallback query routing
persistent session memory with Redis or database
chunk-level citation display
structured logging and observability
automated RAG evaluation