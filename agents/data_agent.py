import os
import google.generativeai as genai
from rag.retriever import retrieve

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
_model = genai.GenerativeModel("gemini-3-flash-preview")

PROMPT_TEMPLATE = """You are a data analyst assistant. The user is asking about structured data (CSVs, financial tables, metrics).

Use the data excerpts below to answer. Be specific with numbers. Identify trends, anomalies, or key figures.
If calculations are needed, show your reasoning.

Data:
{context}

Question: {question}

Analysis:"""

def answer_data_query(query: str) -> dict:
    # Retrieve with higher n to get more data rows
    chunks = retrieve(query, n_results=8)

    if not chunks:
        return {
            "answer": "No data files have been uploaded yet. Please upload a CSV file first.",
            "sources": [],
            "confidence": "low",
        }

    # Prefer CSV sources, but don't exclude docs
    csv_chunks = [c for c in chunks if c["source"].endswith(".csv")]
    selected = csv_chunks if csv_chunks else chunks
    selected = selected[:6]  # cap context size

    context = "\n\n---\n\n".join(
        f"[{c['source']}]\n{c['text']}" for c in selected
    )

    prompt = PROMPT_TEMPLATE.format(context=context, question=query)

    try:
        response = _model.generate_content(prompt)
        answer = response.text.strip()
        confidence = "high" if selected[0]["score"] > 0.6 else "medium"
    except Exception as e:
        answer = f"Error generating analysis: {str(e)}"
        confidence = "low"

    sources = list(dict.fromkeys(c["source"] for c in selected))

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
    }
