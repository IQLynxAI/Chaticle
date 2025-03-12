import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Google Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# FAISS Index File
FAISS_DB_PATH = "vector_store/faiss_index"
