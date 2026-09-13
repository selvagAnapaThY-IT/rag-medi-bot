import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Ensure src directory is in sys.path
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SRC_DIR, ".."))
sys.path.append(SRC_DIR)

from query import ask_rag

app = FastAPI(title="RAG Chatbot API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "RAG Chatbot API is healthy"}

@app.post("/query")
def query_endpoint(req: QueryRequest):
    try:
        result = ask_rag(req.question)
        return result
    except Exception as e:
        return {"error": "Failed to process query", "details": str(e)}

# Serve static frontend files if present (Docker / Production build)
BUILD_DIR = os.path.join(REPO_ROOT, "frontend", "rag-chat-frontend", "build")

if os.path.exists(BUILD_DIR):
    app.mount("/static", StaticFiles(directory=os.path.join(BUILD_DIR, "static")), name="static")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # Serve exact file if exists, otherwise fallback to index.html
        file_path = os.path.join(BUILD_DIR, full_path)
        if full_path and os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(BUILD_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)

