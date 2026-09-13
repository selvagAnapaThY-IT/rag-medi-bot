# src/rag.py
from query import ask_rag

def load_rag_chain():
    """
    Returns a callable QA function using Gemini and FAISS retriever.
    """
    def qa_runner(query_str: str):
        res = ask_rag(query_str)
        return {
            "result": res["answer"],
            "source_documents": res["sources"]
        }
    return qa_runner

