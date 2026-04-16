# DECISIONS.md

## 1. Why I used a simple multi-agent design

I separated the system into:
- Router Agent
- Document Q&A Agent
- Data Analysis Agent

### Reason
This directly matches the assessment requirement for a multi-agent architecture while keeping the logic understandable and modular.

It also makes the system easier to explain in interview because each agent has a clear responsibility.

### Trade-off
A simple router can still misclassify vague prompts such as:
- “summarize”
- “what about this”
- “tell me more”

Even so, I chose clarity and explainability over a more complex orchestration system.

---

## 2. Why I used ChromaDB

I chose **ChromaDB** as the vector store.

### Reason
It is:
- easy to integrate
- lightweight
- local-first
- suitable for free-tier deployment and prototyping

For this take-home assessment, ChromaDB allowed me to focus on the end-to-end workflow instead of spending time on managed vector infrastructure.

### Trade-off
Local persistence is good for a prototype, but not ideal for:
- production durability
- scaling
- multi-instance deployments

If this system were extended, I would likely migrate to a managed vector database.

---

## 3. Why I used Google Gemini

I used **Google Gemini** for answer generation and parts of the routing workflow.

### Reason
It provided a practical API for:
- summarization
- grounded answer generation
- lightweight routing support

It was enough to build a working prototype without adding unnecessary complexity.

### Trade-off
External LLM usage introduces:
- quota limits
- timeout risk
- dependency on provider availability

Because of that, I treated graceful fallback and honest failure handling as important design considerations.

---

## 4. Why I kept session memory simple

I chose a lightweight `session_id`-based approach rather than building full persistent chat memory.

### Reason
The assessment requires support for follow-up queries within a conversation session, and simple in-memory history is enough to demonstrate that behavior.

This keeps the implementation small and easy to explain.

### Trade-off
This design:
- does not survive backend restarts
- is not durable
- is not production-grade for long-lived conversations

If I extended the project, I would move session storage to Redis or a database.

---

## 5. Why I used React + Vite for the frontend

I chose **React + Vite** for the frontend.

### Reason
This gave me:
- fast iteration
- easy deployment
- a clean modern UI
- simple environment-variable handling

It was a strong fit for building a small but polished interface quickly.

### Trade-off
I prioritized clarity and demo-readiness over advanced frontend features such as:
- multi-file management
- persistent local chat state
- richer pagination or workspace controls

---

## 6. Why I prioritized working deployment over advanced extras

I focused first on getting a working deployed system online.

### Reason
The assessment emphasizes:
- a working system
- clean design
- explainable decisions
- live deployment

So I prioritized:
- upload flow
- question answering flow
- deployment
- API correctness

before optional enhancements.

### Trade-off
This meant some bonus features were left lighter than they could be, such as:
- advanced evaluation
- richer observability
- stronger citation fidelity

---

## 7. Why I used realistic synthetic project documents

I used realistic synthetic project-style documents including:
- project status reports
- risk registers
- delays
- budget information
- missing or inconsistent values

### Reason
This better reflects the type of messy internal documentation a project intelligence assistant would need to handle in real usage.

It also helps demonstrate that the system is designed for realistic project questioning, not just ideal clean text.

### Trade-off
The dataset is still relatively small and curated for demo purposes, so it is useful for functional validation but not enough for large-scale benchmarking.

---

## 8. Why I used a simple chunking strategy

I used recursive character-based chunking with overlap.

### Reason
This is a reliable default for many document types and helped preserve local context without over-engineering the ingestion pipeline.

It is also easy to explain and defend in interview.

### Trade-off
This approach is not specialized for every layout type, especially:
- tables
- mixed-format reports
- highly structured financial sheets

If extended, I would improve chunking based on document type.

---

## 9. Why I separated document and data workflows

I treated document-style questions and data-style questions differently.

### Reason
Project documents often contain both:
- narrative explanation
- numeric and structured data

By separating these workflows, I could tailor prompts and retrieval behavior better for each case.

### Trade-off
The boundary between “document” and “data” is not always perfect, so some questions can sit between both categories.

Still, I preferred explicit separation because it improves clarity and modularity.

---

## 10. Why I chose free-tier deployment tools

I deployed:
- frontend on Vercel
- backend on Render

### Reason
These platforms are fast to set up, easy to demo, and sufficient for a take-home assessment.

They also support the project’s architecture without extra infrastructure overhead.

### Trade-off
Free-tier deployment introduces:
- cold starts
- slower first response after inactivity
- less predictable performance than paid infrastructure

For an assessment prototype, this is acceptable.

---

## 11. What I would improve next

If I had more time, I would improve:

### Routing
- stronger rule-based routing before LLM fallback
- better handling of vague prompts

### Retrieval
- improved chunking for mixed document types
- stronger source attribution

### Reliability
- persistent session memory
- structured logging
- better fallback responses

### Evaluation
- automated test queries
- RAGAS-style evaluation
- latency and answer-quality measurements

---

## 12. Final Reflection

The overall design intentionally favors:
- simplicity
- explainability
- modular code
- a working end-to-end deployment

I believe this is the right trade-off for the assessment because a clean, functional system that I can defend confidently is more valuable than a more complex design that is harder to explain or maintain.