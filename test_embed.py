import os
import time
from dotenv import load_dotenv

print("STEP 1: script started")

load_dotenv()
print("STEP 2: .env loaded")
print("GOOGLE_API_KEY exists:", bool(os.getenv("GOOGLE_API_KEY")))

t = time.time()
from langchain_google_genai import GoogleGenerativeAIEmbeddings
print("STEP 3: import done in", round(time.time() - t, 2), "seconds")

t = time.time()
emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
print("STEP 4: embedder created in", round(time.time() - t, 2), "seconds")

t = time.time()
vec = emb.embed_query("hello world")
print("STEP 5: embed_query success in", round(time.time() - t, 2), "seconds")
print("Embedding length:", len(vec))