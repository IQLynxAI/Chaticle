import google.generativeai as genai
from config import GEMINI_API_KEY
from services.vector_db import vector_db

class GeminiService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)

    def generate_response(self, user_question: str, relevant_content):
        # Retrieve last 5 messages from chat history
        chat_history = vector_db.get_chat_history()

        # Format chat history for Gemini
        history_text = "\n".join([f"User: {msg['user']}\nBot: {msg['bot']}" for msg in chat_history])

        # Prepare Gemini prompt
        prompt = f"""
            You are a helpful AI assistant. Answer the user's question based on the following knowledge:

            Past conversation:
            {history_text}

            Webpage content:
            {relevant_content}

            User question: {user_question}
            """

        # Generate response using Gemini
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        # ✅ Fix: Extract only the text from the response
        if hasattr(response, "text"):
            return response.text  # Extract plain text response
        else:
            return "⚠️ Error: Unexpected response format from Gemini."

gemini_service = GeminiService()
