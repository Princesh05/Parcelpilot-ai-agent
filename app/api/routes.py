from fastapi import FastAPI

from app.agent.agent import ParcelPilotAgent
from app.api.schemas import ChatRequest, ChatResponse


app = FastAPI(
    title="ParcelPilot AI Agent",
    description="AI-powered customer support agent for ParcelPilot",
    version="1.0.0"
)


agent = ParcelPilotAgent()


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "ParcelPilot AI Agent"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        result = agent.chat(
            message=request.message,
            user_context=request.user_context
        )

        return result

    except Exception as e:

        return ChatResponse(
            success=False,
            answer="I'm temporarily unable to process your request. Please try again later.",
            error=str(e),
            tool_history=[]
        )