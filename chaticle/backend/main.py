from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import ContentRequest, QuestionRequest
from services.vector_db import vector_db
from services.gemini_service import gemini_service

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/store_content")
async def store_content(request: ContentRequest):
    """
    Stores the extracted webpage content in the vector database.
    """
    logger.info("🔹 Received content to store.")

    try:
        vector_db.store_document(request.content)
        logger.info("✅ Content successfully stored in vector database.")
        return {"message": "Content stored successfully"}
    except Exception as e:
        logger.error(f"❌ Error storing content: {str(e)}")
        return {"error": "Failed to store content"}, 500


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Retrieves relevant content from vector DB and generates AI response.
    """
    user_question = request.question
    logger.info(f"🤖 Received Question: {request.question}")

    try:
        relevant_content = vector_db.search(user_question, top_k=3)
        response = gemini_service.generate_response(user_question, relevant_content)

        logger.info(f"✅ AI Response generated")
        return {"answer": response}

    except Exception as e:
        logger.error(f"❌ Error generating response: {str(e)}")
        return {"error": "Failed to generate response"}, 500


if __name__ == "__main__":
    import uvicorn

    logger.info("🚀 FastAPI Server is starting...")
    uvicorn.run(app, host="127.0.0.1", port=8000)