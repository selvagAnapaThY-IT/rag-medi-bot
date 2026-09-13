# 🩻 MediBot AI - Medical PDF RAG System

MediBot AI is a Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **LangChain**, **FAISS**, **Google Gemini AI**, and **React**. It parses medical and clinical PDF documents, embeds them using HuggingFace embeddings, and provides intelligent Q&A with source citations.

---

## 📁 Project Structure

```
rag/
├── Dockerfile          # Multi-stage Docker build for Render deployment
├── .dockerignore       # Docker build exclusions
├── src/
│   ├── app.py          # FastAPI server & static file serving
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

## 🚀 How to Deploy on Render using Docker

1. **Push your code to GitHub** (Ensure latest changes are pushed).

2. **Log into Render**:
   Go to [dashboard.render.com](https://dashboard.render.com/) and click **New +** -> **Web Service**.

3. **Connect Repository**:
   Select your GitHub repository: `selvagAnapaThY-IT/rag-medi-bot`.

4. **Configure Web Service**:
   - **Name**: `rag-medi-bot` (or your preferred name)
   - **Language**: `Docker`
   - **Region**: Choose nearest region (e.g. Oregon, Singapore, Frankfurt)
   - **Branch**: `main`
   - **Dockerfile Path**: `./Dockerfile`

5. **Set Environment Variables**:
   Under **Environment Variables**, add:
   - Key: `GOOGLE_API_KEY`
   - Value: `YOUR_ACTUAL_GEMINI_API_KEY`

6. **Deploy**:
   Click **Create Web Service**. Render will automatically:
   - Build the React frontend production bundle.
   - Install Python backend dependencies.
   - Launch your FastAPI server on Render's assigned `$PORT`.

Once deployed, visit your Render `.onrender.com` URL to use the full application!

---

## 💻 Local Development

### Backend
```bash
python -m venv rag_env
.\rag_env\Scripts\activate
pip install -r requirements.txt
python src/app.py
```

### Frontend
```bash
cd frontend/rag-chat-frontend
npm install
npm start
```
