import faiss
import numpy as np
import os
import json
from sentence_transformers import SentenceTransformer
from config import FAISS_DB_PATH, EMBEDDING_MODEL


class VectorDatabase:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None
        self.documents = []
        self.chat_history = []  # Store chat messages
        self.load_or_create_index()

    def load_or_create_index(self):
        os.makedirs(os.path.dirname(FAISS_DB_PATH), exist_ok=True)

        if os.path.exists(FAISS_DB_PATH):
            print("🔹 Loading FAISS index...")
            self.index = faiss.read_index(FAISS_DB_PATH)
            with open(FAISS_DB_PATH + ".json", "r") as f:
                self.documents = json.load(f)
        else:
            print("🔹 Creating new FAISS index...")
            self.index = faiss.IndexFlatL2(384)  # Vector size (MiniLM has 384 dims)
            self.documents = []

    def store_document(self, content: str):
        print("⚠️ Resetting FAISS index before storing new content...")

        self.index = faiss.IndexFlatL2(384)  # Reset FAISS index
        self.documents = []
        self.chat_history = []  # Clear chat history when storing new content

        embedding = self.model.encode([content])[0]
        self.index.add(np.array([embedding], dtype=np.float32))
        self.documents.append(content)

        os.makedirs(os.path.dirname(FAISS_DB_PATH), exist_ok=True)
        faiss.write_index(self.index, FAISS_DB_PATH)
        with open(FAISS_DB_PATH + ".json", "w") as f:
            json.dump(self.documents, f)

    def store_chat(self, user_message: str, bot_response: str):
        """Store the conversation history"""
        self.chat_history.append({"user": user_message, "bot": bot_response})

    def get_chat_history(self):
        """Retrieve last N messages for context"""
        return self.chat_history[-5:]  # Last 5 messages as context

    def search(self, query: str, top_k=3):
        if len(self.documents) == 0:
            return ["No relevant information found. Try opening the extension on a webpage first."]

        query_embedding = self.model.encode([query])[0]
        distances, indices = self.index.search(np.array([query_embedding], dtype=np.float32), top_k)
        results = [self.documents[idx] for idx in indices[0] if idx < len(self.documents)]
        return results


vector_db = VectorDatabase()
