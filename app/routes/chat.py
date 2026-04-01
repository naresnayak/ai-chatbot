import uuid
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.gemini_service import GeminiService
from app.services.chat_manager import ChatManager

# Create the router
router = APIRouter()

# Initialize services
gemini = GeminiService()
manager = ChatManager()

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """Handles the streaming AI chat response and history persistence."""
    session_id = request.session_id or str(uuid.uuid4())
    
    # Fetch history from the Manager (Mongo/Redis)
    history = await manager.get_history(session_id)
    
    async def generate():
        full_response = ""
        # Stream chunks from Gemini
        async for chunk in gemini.stream_response(history, request.message):
            full_response += chunk
            yield f"{chunk}\n"
        
        # Save both turns to history after stream completion
        await manager.update_history(session_id, "user", request.message)
        await manager.update_history(session_id, "model", full_response)

    return StreamingResponse(
        generate(), 
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )