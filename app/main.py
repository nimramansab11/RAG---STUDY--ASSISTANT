from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.rag_service import RAGService
from app.models import QuestionRequest, AnswerResponse


# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------

app = FastAPI(
    title="StudySpace AI",
    description="AI Study Assistant powered by RAG",
    version="1.0.0"
)


# --------------------------------------------------
# RAG SERVICE
# --------------------------------------------------

print("Starting StudySpace AI...")

rag = RAGService()

print("StudySpace AI is ready.")


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/")
async def home():
    return FileResponse(
        "static/index.html"
    )


# --------------------------------------------------
# ASK AI
# --------------------------------------------------

@app.post(
    "/api/ask",
    response_model=AnswerResponse
)
async def ask_question(
    request: QuestionRequest
):

    result = rag.ask(
        request.question
    )

    return result


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "documents": rag.collection.count()
    }