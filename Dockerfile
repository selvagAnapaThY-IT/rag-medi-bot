# Step 1: Build React Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/rag-chat-frontend/package*.json ./
RUN npm install

COPY frontend/rag-chat-frontend/ ./
RUN DISABLE_ESLINT_PLUGIN=true npm run build

# Step 2: Python FastAPI Backend & Final Image
FROM python:3.10-slim

WORKDIR /app

# Prevent Python from writing .pyc and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and pre-built frontend
COPY . ./
COPY --from=frontend-builder /app/frontend/build ./frontend/rag-chat-frontend/build

EXPOSE 8000

# Run FastAPI backend server (listens on $PORT set by Render)
CMD ["python", "src/app.py"]
