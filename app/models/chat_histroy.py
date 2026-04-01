from pydantic import BaseModel, Field
from datetime import datetime

class ChatMessage(BaseModel):
    user_id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True