import os
import time

import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
COLLECTION_NAME = "project_docs"

_client = None
_collection = None
_embedder = None


def _get_collection():
    global _client, _collection

    if _collection is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    return _collection


def _get_embedder():
    global _embedder

    if _embedder is None:
        if not os.getenv("GOOGLE_API_KEY"):
            raise RuntimeError("GOOGLE_API_KEY is missing in environment variables.")

        _embedder = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

    return _embedder


def _is_retryable_embedding_error(error: Exception) -> bool:
    message = str(error).lower()

    retry_signals = [
        "deadline exceeded",
        "504",
        "timed out",
        "timeout",
        "service unavailable",
        "503",
        "connection reset",
        "temporarily unavailable",
    ]

    return any(signal in message for signal in retry_signals)


def _to_plain_vector(vector) -> list[float]:
    return [float(x) for x in list(vector)]


def _embed_query_with_retry(query: str, retries: int = 3, base_sleep: int = 2) -> list[float]:
    embedder = _get_embedder()
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            raw_vector = embedder.embed_query(query)
            return _to_plain_vector(raw_vector)
        except Exception as e:
            last_error = e
            print(f"[QUERY EMBED RETRY] attempt={attempt}/{retries} error={e}")

            if not _is_retryable_embedding_error(e):
                raise

            if attempt < retries:
                time.sleep(base_sleep * attempt)

    raise last_error


def retrieve(query: str, n_results: int = 5) -> list[dict]:
    """
    Returns a list of dicts with:
    - text
    - source
    - score
    Returns [] if collection is empty.
    """
    collection = _get_collection()

    if collection.count() == 0:
        return []

    query_embedding = _embed_query_with_retry(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        score = round(1 - dist, 3)

        chunks.append(
            {
                "text": doc,
                "source": meta.get("source", "unknown"),
                "score": score,
            }
        )

    return chunks