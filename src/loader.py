import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Define paths relative to repo root
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SRC_DIR, ".."))

# Search for data folder in src/faiss_index/data, src/data, or data
DATA_DIRS = [
    os.path.join(SRC_DIR, "faiss_index", "data"),
    os.path.join(SRC_DIR, "data"),
    os.path.join(REPO_ROOT, "data"),
]

data_dir = None
for d in DATA_DIRS:
    if os.path.exists(d):
        data_dir = d
        break

if not data_dir:
    raise FileNotFoundError(f"Could not find data directory containing PDFs. Searched: {DATA_DIRS}")

print(f"Loading PDFs from directory: {data_dir}")

documents = []
for file in os.listdir(data_dir):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(data_dir, file)
        print(f"Loading: {file}...")
        try:
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
        except Exception as e:
            print(f"Warning: Failed to load {file}: {e}")

if not documents:
    raise ValueError("No PDF documents were successfully loaded!")

print(f"Total documents loaded: {len(documents)}. Splitting text...")

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

print(f"Generated {len(chunks)} text chunks. Generating embeddings...")

# Use local embeddings
emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, emb)

# Save vectorstore consistently to src/faiss_index
output_index_path = os.path.join(SRC_DIR, "faiss_index")
vectorstore.save_local(output_index_path)
print(f"Vectorstore created successfully and saved to '{output_index_path}'.")