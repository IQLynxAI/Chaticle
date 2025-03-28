import google.generativeai as genai
from config import GEMINI_API_KEY
from services.vector_db import vector_db
import re

class GeminiService:
    """
    A service class to interact with the Gemini API for generating AI responses.
    """
    def __init__(self):
        """
        Initializes the GeminiService by configuring the API key.
        """
        genai.configure(api_key=GEMINI_API_KEY)

    def generate_response(self, user_question: str, relevant_content):
        """
        Generates a response to the user's question using the Gemini API.

        Args:
            user_question (str): The question asked by the user.
            relevant_content: The relevant content retrieved from the vector database.

        Returns:
            str: The formatted response generated by Gemini.
        """
        chat_history = vector_db.get_chat_history()

        history_text = "\n".join([f"User: {msg['user']}\nBot: {msg['bot']}" for msg in chat_history])

        prompt = f"""
            You are a helpful AI assistant. Answer the user's question based on the following knowledge:

            Past conversation:
            {history_text}

            Webpage content:
            {relevant_content}

            User question: {user_question}
            """

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        response_text = response.text

        formatted_response = self.format_code_blocks(response_text)

        return formatted_response

    def format_code_blocks(self, text):
        """
        Formats code blocks in the response text by wrapping them in <pre><code> tags.

        Args:
            text (str): The response text containing code blocks.

        Returns:
            str: The formatted text with code blocks wrapped in HTML tags.
        """
        formatted_text = re.sub(
            r'```.*?\n(.*?)```',
            lambda match: f'<pre><code>{match.group(1).strip()}</code></pre>',
            text,
            flags=re.DOTALL
        )
        return formatted_text

gemini_service = GeminiService()