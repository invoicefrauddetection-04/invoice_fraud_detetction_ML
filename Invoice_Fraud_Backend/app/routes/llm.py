from fastapi import APIRouter
from pydantic import BaseModel

from app.services.llm_service import generate_ai_explanation

router = APIRouter(
    prefix="/llm",
    tags=["LLM"]
)


class LLMRequest(BaseModel):
    document_id: int
    question: str


@router.post("/chat")
def chat(request: LLMRequest):
    return generate_ai_explanation(
        document_id=request.document_id,
        question=request.question
    )