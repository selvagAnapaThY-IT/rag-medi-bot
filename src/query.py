# rag_query.py
import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(REPO_ROOT, ".env"))

# Resolve FAISS path. Check repo-root/src/faiss_index then repo-root/faiss_index
FAISS_PATH = os.path.join(REPO_ROOT, "src", "faiss_index")
if not os.path.exists(FAISS_PATH):
    FAISS_PATH = os.path.join(REPO_ROOT, "faiss_index")
if not os.path.exists(FAISS_PATH):
    FAISS_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")

if not os.path.exists(FAISS_PATH):
    raise FileNotFoundError(
        f"FAISS index not found at '{FAISS_PATH}'. Run loader.py to create it."
    )

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    FAISS_PATH,
    embeddings=embeddings,
    allow_dangerous_deserialization=True,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GOOGLE_API_KEY,
)


def ask_rag(question: str):
    """Given a question, return RAG answer and sources."""
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



