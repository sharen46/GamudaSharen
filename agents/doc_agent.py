import os
import google.generativeai as genai
from rag.retriever import retrieve

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
_model = genai.GenerativeModel("gemini-3-flash-preview")

PROMPT_TEMPLATE = """You are a project intelligence assistant answering questions about internal documents.

Use ONLY the context below to answer. If the answer isn't in the context, say so clearly.
Always cite the source document name when referencing information.

Context:
{context}

Question: {question}

Answer (be concise, cite sources inline like [source.pdf]):"""

def answer_doc_query(query: str) -> dict:
    chunks = retrieve(query, n_results=5)

    if not chunks:
        return {
            "answer": "No documents have been uploaded yet. Please upload some files first.",
            "sources": [],
            "confidence": "low",
        }

    # Filter low-relevance chunks (cosine similarity < 0.3)
    relevant = [c for c in chunks if c["score"] >= 0.3]
    if not relevant:
        relevant = chunks[:2]  # always use top 2 as fallback

    context = "\n\n---\n\n".join(
        f"[{c['source']}]\n{c['text']}" for c in relevant
    )

    prompt = PROMPT_TEMPLATE.format(context=context, question=query)

    try:
        response = _model.generate_content(prompt)
        answer = response.text.strip()
        confidence = "high" if relevant[0]["score"] > 0.7 else "medium" if relevant[0]["score"] > 0.4 else "low"
    except Exception as e:
        answer = f"Error generating answer: {str(e)}"
        confidence = "low"

    sources = list(dict.fromkeys(c["source"] for c in relevant))  # deduplicated, ordered

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
    }
