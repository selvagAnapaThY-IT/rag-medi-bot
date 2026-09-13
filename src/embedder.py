# src/embedder.py
from langchain.embeddings import SentenceTransformerEmbeddings

def get_embeddings():
    """
    Returns a local embedding model (SentenceTransformer).
    Replace with Gemini embeddings later if needed.
    """
    return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
