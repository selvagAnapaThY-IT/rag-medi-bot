# 🩻 MediBot AI - Medical PDF RAG System

MediBot AI is a Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **LangChain**, **FAISS**, **Google Gemini AI**, and **React**. It parses medical and clinical PDF documents, embeds them using HuggingFace embeddings, and provides intelligent Q&A with source citations.

---

## 📁 Project Structure

```
rag/
├── src/
│   ├── app.py          # FastAPI server endpoints (/query)
│   ├── query.py        # RAG pipeline with FAISS retriever & Gemini LLM
│   ├── loader.py       # PDF document loader & FAISS vectorstore generator
│   ├── rag.py          # RAG chain wrapper
│   ├── chat.py         # Terminal CLI chat interface
│   └── faiss_index/    # FAISS index storage & PDF data directory
├── frontend/
│   └── rag-chat-frontend/   # React frontend UI
├── .env.example        # Environment variable template
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Backend Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/selvagAnapaThY-IT/rag-medi-bot.git
   cd rag-medi-bot
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   python -m venv rag_env
   # On Windows:
   .\rag_env\Scripts\activate
   # On macOS/Linux:
   source rag_env/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**:
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   ```

5. **Generate Vectorstore**:
   Place PDF documents inside `src/faiss_index/data/` and run:
   ```bash
   python src/loader.py
   ```

6. **Start FastAPI Backend**:
   ```bash
   python -m uvicorn src.app:app --reload --port 8000
   ```
   The backend API will run at `http://127.0.0.1:8000`.

---

### 2. Frontend Setup

1. **Navigate to Frontend Directory**:
   ```bash
   cd frontend/rag-chat-frontend
   ```

2. **Install Dependencies & Start React Server**:
   ```bash
   npm install
   npm start
   ```
   The React UI will run at `http://localhost:3000`.

---

### 3. Terminal CLI Chat Mode (Optional)

If you prefer to chat directly in your terminal:
```bash
python src/chat.py
```
