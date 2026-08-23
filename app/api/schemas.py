from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    user_context: dict


class ChatResponse(BaseModel):
    success: bool
    answer: str | None = None
    error: str | None = None
    tool_history: list = []