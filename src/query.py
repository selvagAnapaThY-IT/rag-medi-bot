# rag_query.py
import os
import sys
import subprocess
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(REPO_ROOT, ".env"))

_vectorstore = None
_retriever = None

def get_faiss_path():
    possible_paths = [
        os.path.join(REPO_ROOT, "src", "faiss_index"),
        os.path.join(REPO_ROOT, "faiss_index"),
        os.path.join(os.path.dirname(__file__), "faiss_index"),
    ]
    for p in possible_paths:
        if os.path.exists(p) and (os.path.exists(os.path.join(p, "index.faiss")) or os.path.exists(os.path.join(p, "index.pkl"))):
            return p
    return possible_paths[0]

def get_retriever():
    global _vectorstore, _retriever
    if _retriever is not None:
        return _retriever

    faiss_path = get_faiss_path()

    # If FAISS index does not exist, check if we can run loader.py automatically
    index_file = os.path.join(faiss_path, "index.faiss")
    if not os.path.exists(index_file):
        print(f"FAISS index not found at '{faiss_path}'. Attempting auto-generation using loader.py...")
        loader_script = os.path.join(os.path.dirname(__file__), "loader.py")
        if os.path.exists(loader_script):
            try:
                subprocess.run([sys.executable, loader_script], check=True)
            except Exception as e:
                print(f"Warning: Auto-generating index via loader.py failed: {e}")

    if not os.path.exists(faiss_path):
        raise FileNotFoundError(
            f"FAISS index not found at '{faiss_path}'. Run loader.py or commit pre-built index."
        )

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    _vectorstore = FAISS.load_local(
        faiss_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )
    _retriever = _vectorstore.as_retriever(search_kwargs={"k": 3})
    return _retriever

def get_llm():
    google_api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=google_api_key,
    )

def ask_rag(question: str):
    """Given a question, return RAG answer and sources."""
    retriever = get_retriever()
    llm = get_llm()

    docs = retriever.invoke(question)
    if not docs:
        return {"answer": "No relevant information found in the documents.", "sources": []}
    
    context = "\n\n".join([doc.page_content for doc in docs])
    raw_sources = [doc.metadata.get("source", "unknown") for doc in docs]
    # Clean source paths to show readable filenames
    sources = list(set([os.path.basename(s) for s in raw_sources]))

    prompt = f"""Using the following text extracted from medical PDFs, answer the question accurately and concisely.

Text Context:
{context}

Question: {question}
Answer:"""

    response = llm.invoke(prompt)
    return {"answer": response.content, "sources": sources}




