import os
import re
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
_model = genai.GenerativeModel("gemini-3-flash-preview")

SYSTEM_PROMPT = """You are a query router for a project intelligence assistant.

Classify the user's query as either:
- "doc"  → questions about project status, risks, reports, documents, PDFs, written content
- "data" → questions about numbers, metrics, trends, CSV data, financial figures, statistics

Reply with ONLY one word: doc or data. Nothing else."""

DATA_HINTS = {
    "budget", "cost", "financial", "finance", "claim", "certified", "retention",
    "variation", "vo", "amount", "rm", "progress %", "percentage", "trend",
    "metrics", "numbers", "figure", "table", "csv", "excel", "spreadsheet",
    "statistics", "how much", "compare", "total", "sum", "average"
}

DOC_HINTS = {
    "risk", "issue", "status", "report", "document", "pdf", "milestone",
    "delay", "schedule", "forecast", "behind", "ahead", "action", "plan"
}

def _rule_route(query: str) -> str | None:
    q = query.lower()

    data_score = 0
    doc_score = 0

    for hint in DATA_HINTS:
        if hint in q:
            data_score += 1

    for hint in DOC_HINTS:
        if hint in q:
            doc_score += 1

    if re.search(r"\b(rm|\d+%|\d+\.\d+|\d{1,3}(,\d{3})+)\b", q):
        data_score += 2

    if data_score > doc_score:
        return "data"
    if doc_score > data_score:
        return "doc"
    return None

def route_query(query: str) -> str:
    rule_label = _rule_route(query)
    if rule_label:
        return rule_label

    try:
        response = _model.generate_content(f"{SYSTEM_PROMPT}\n\nQuery: {query}")
        label = response.text.strip().lower()
        return "data" if label == "data" else "doc"
    except Exception:
        return "doc"