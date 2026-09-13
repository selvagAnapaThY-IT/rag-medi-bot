import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure src directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query import ask_rag

app = FastAPI(title="RAG Chatbot API")

# Enable CORS for React Frontend (typically running on port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "RAG Chatbot API is running"}

@app.post("/query")
def query_endpoint(req: QueryRequest):
    try:
        result = ask_rag(req.question)
        return result
    except Exception as e:
        return {"error": "Failed to process query", "details": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
