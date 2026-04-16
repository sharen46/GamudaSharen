import hashlib
import os
import time
import traceback

import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    CSVLoader,
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
)
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


def _load_file(path: str, original_filename: str):
    ext = os.path.splitext(original_filename)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(path)
    elif ext == ".csv":
        loader = CSVLoader(path)
    elif ext == ".docx":
        loader = Docx2txtLoader(path)
    elif ext == ".txt":
        loader = TextLoader(path, encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return loader.load()


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


def _to_plain_embeddings(embeddings) -> list[list[float]]:
    return [_to_plain_vector(vec) for vec in embeddings]


def _embed_with_retry(
    texts: list[str],
    batch_size: int = 1,
    retries: int = 3,
    base_sleep: int = 2,
) -> list[list[float]]:
    embedder = _get_embedder()
    all_embeddings: list[list[float]] = []

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        last_error = None

        for attempt in range(1, retries + 1):
            try:
                raw_embeddings = embedder.embed_documents(batch)
                plain_embeddings = _to_plain_embeddings(raw_embeddings)
                all_embeddings.extend(plain_embeddings)
                last_error = None
                break
            except Exception as e:
                last_error = e
                print(
                    f"[EMBED RETRY] batch={start // batch_size} "
                    f"attempt={attempt}/{retries} error={e}"
                )

                if not _is_retryable_embedding_error(e):
                    raise

                if attempt < retries:
                    time.sleep(base_sleep * attempt)

        if last_error is not None:
            raise last_error

    return all_embeddings


def ingest_file(tmp_path: str, original_filename: str) -> dict:
    try:
        print(f"[INGEST] Loading file: {original_filename}")

        docs = _load_file(tmp_path, original_filename)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""],
        )

        chunks = splitter.split_documents(docs)
        valid_chunks = [
            chunk for chunk in chunks
            if chunk.page_content and chunk.page_content.strip()
        ]

        if not valid_chunks:
            return {"chunks": 0, "doc_id": None}

        doc_id = hashlib.md5(original_filename.encode("utf-8")).hexdigest()[:12]
        texts = [chunk.page_content.strip() for chunk in valid_chunks]

        print(f"[INGEST] Total chunks: {len(texts)}")

        embeddings = _embed_with_retry(
            texts=texts,
            batch_size=1,
            retries=3,
            base_sleep=2,
        )

        collection = _get_collection()
        collection.upsert(
            ids=[f"{doc_id}_{i}" for i in range(len(valid_chunks))],
            embeddings=embeddings,
            documents=texts,
            metadatas=[
                {
                    "source": original_filename,
                    "doc_id": doc_id,
                    "chunk_index": i,
                    **(
                        {k: str(v) for k, v in valid_chunks[i].metadata.items()}
                        if valid_chunks[i].metadata
                        else {}
                    ),
                }
                for i in range(len(valid_chunks))
            ],
        )

        return {"chunks": len(valid_chunks), "doc_id": doc_id}

    except Exception as e:
        print("[INGEST ERROR]", repr(e))
        traceback.print_exc()
        raise