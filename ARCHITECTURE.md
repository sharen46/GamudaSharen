# ARCHITECTURE.md

## 1. System Overview

This project is an **AI-Powered Project Intelligence Assistant** that ingests project documents and answers questions about project status, risks, budgets, and schedules using a **multi-agent Retrieval-Augmented Generation (RAG)** workflow.

The system is designed to be:
- simple
- modular
- explainable
- deployable on free-tier services

It supports:
- document upload
- chunking and embedding
- vector retrieval
- query routing
- answer generation
- lightweight session-based follow-up support

The overall design intentionally favors a working end-to-end prototype that is easy to explain and extend.

---

## 2. Main Components

### 2.1 Frontend

The frontend is built with **React + Vite** and provides:
- file upload
- question input
- answer display
- source display
- confidence display
- simple chat history

The UI is intentionally minimal so the user can move through the flow quickly:

1. upload a file  
2. ask a question  
3. read the answer

This keeps the interaction simple and demo-friendly.

### 2.2 Backend

The backend is built with **FastAPI** and exposes the main API endpoints:
- `GET /health`
- `POST /upload`
- `POST /chat`

The backend handles:
- file ingestion
- document indexing
- routing logic
- retrieval
- answer generation
- lightweight session handling

### 2.3 Ingestion Pipeline

When a user uploads a document:

1. the backend loads the file
2. extracts the text
3. splits it into chunks
4. generates embeddings
5. stores embeddings and metadata in ChromaDB

Supported file types include:
- PDF
- CSV
- TXT

This pipeline allows uploaded project documents to become searchable by meaning rather than exact keyword matching.

### 2.4 Vector Store

The project uses **ChromaDB** as the vector database.

It stores:
- chunk text
- embeddings
- document source metadata
- chunk index metadata

This allows the retriever to fetch relevant context for user questions.

I chose ChromaDB because it is a lightweight local vector store that is easy to integrate for rapid prototyping. It avoids the setup overhead of a managed external vector database and is sufficient for a take-home assessment prototype.

### 2.5 Router Agent

The Router Agent classifies the user query into one of two paths:
- `doc`
- `data`

#### Document Q&A Agent
Used for:
- project reports
- risk registers
- narrative project documents
- status updates
- PDF-based summarization

#### Data Analysis Agent
Used for:
- numeric questions
- tables
- metrics
- trends
- structured data interpretation

This separation makes the system easier to explain, debug, and extend.

In the current implementation, routing is handled by an LLM-based classifier with a safe fallback path. This design keeps responsibilities separated, while accepting that vague prompts may still be misclassified.

### 2.6 Retriever

The Retriever:

1. embeds the incoming query
2. searches ChromaDB
3. returns the most relevant chunks

Each retrieved chunk includes:
- text
- source
- similarity score

This retrieved context is passed to the selected agent before final answer generation.

### 2.7 LLM Layer

The system uses **Google Gemini** for:
- routing fallback
- answer generation
- summarization
- synthesis from retrieved chunks

The LLM does not answer from memory alone. It uses retrieved document context to ground responses.

---

## 3. Data Flow

### 3.1 Upload Flow

1. User selects a file in the frontend  
2. Frontend sends file to `POST /upload`  
3. Backend loads and chunks document  
4. Embeddings are generated  
5. Chunks are stored in ChromaDB  
6. Backend returns upload success metadata  

### 3.2 Question Flow

1. User enters a question in the frontend  
2. Frontend sends it to `POST /chat`  
3. Backend routes the query  
4. Selected agent retrieves relevant chunks  
5. LLM generates answer from retrieved context  
6. Backend returns:
   - answer
   - agent used
   - sources
   - confidence
7. Frontend displays the result  

### 3.3 Follow-Up Flow

The API includes a `session_id` field to support follow-up conversation design.

In the prototype, session handling is lightweight and intended mainly for demonstration rather than durable long-term conversation memory.

This allows the architecture to support follow-up style questions such as:
- “What about the budget?”
- “Compare it with Alpha”
- “What are the risks?”

while keeping the implementation simple.

---

## 4. Chunking Strategy

The ingestion pipeline uses **RecursiveCharacterTextSplitter** with a **1000-character chunk size** and overlap.

### Reason
This helps:
- preserve local context
- reduce loss of meaning between chunks
- improve retrieval quality
- keep chunks small enough for embeddings and prompts

This is useful for project reports where related status information often appears in the same paragraph or short section.

### Trade-off
This is a practical strategy for prototype-scale documents, but it is not yet optimized for all layout types, especially:
- tables
- mixed-format reports
- more complex spreadsheets

---

## 5. Technology Choices

### FastAPI
Chosen because it is:
- lightweight
- easy to deploy
- well-suited for REST APIs
- fast to prototype

### React + Vite
Chosen because it provides:
- fast development
- simple deployment
- clean frontend structure
- strong support for environment variables and modern builds

### ChromaDB
Chosen because it is:
- simple
- local-first
- free-tier friendly
- sufficient for prototype RAG workflows

### LangChain
Chosen mainly to simplify:
- document loading
- embeddings integration
- retrieval workflow

### Google Gemini
Chosen because it:
- is easy to integrate
- supports useful generation quality
- is sufficient for prototype routing and QA workflows

---

## 6. Session Handling

The system includes a lightweight session mechanism using `session_id`.

### Current Design
- recent conversation turns can be associated with a session
- follow-up questions can reuse earlier context
- suitable for demo and assessment use

### Limitation
This is not durable across restarts and is not intended as a production chat memory solution.

If extended further, session state should be persisted in Redis or a database.

---

## 7. Deployment Architecture

### Frontend
Hosted on **Vercel**

### Backend
Hosted on **Render**

### Notes
- frontend and backend are deployed separately
- frontend uses `VITE_API_BASE_URL` to connect to the backend
- backend uses environment variables such as `GOOGLE_API_KEY`
- free-tier cold starts may delay the first request

This deployment setup is sufficient for a take-home assessment and public demo.

---

## 8. Failure Handling

The architecture is designed with practical fallback behavior in mind:

- router can fall back safely if classification fails
- retrieval can fail gracefully
- low-confidence answers can still be returned honestly
- external provider failures do not have to fully break the user flow

This matters because embedding and generation are external API-dependent steps.

The system prioritizes honest prototype behavior over hiding failures.

---

## 9. Limitations

Current limitations include:
- local ChromaDB persistence is prototype-oriented
- session handling is lightweight and not durable
- vague prompts can still be routed incorrectly
- citations are document-level in the UI
- free-tier deployment can introduce cold-start delays

These trade-offs were accepted to keep the solution simple, working, and explainable.

---

## 10. Possible Improvements

If extended further, I would improve:
- routing robustness with stronger rules + fallback classification
- chunk-level citations
- persistent conversation memory using Redis or a database
- observability and latency logging
- automated RAG evaluation
- managed vector database for production durability

I would also improve handling for mixed document structures such as dense tables and spreadsheet-heavy analysis.

---

## 11. Conclusion

This architecture intentionally prioritizes:
- working end-to-end behavior
- clarity
- modularity
- explainability

It meets the goal of building a deployable multi-agent RAG prototype while remaining simple enough to defend in a live technical interview.

The system demonstrates document ingestion, vector retrieval, multi-agent routing, grounded answer generation, and full-stack deployment in a practical assessment-ready form.