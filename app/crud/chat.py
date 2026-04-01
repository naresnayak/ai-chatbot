from app.database import db_helper
from app.models.chat_histroy import ChatMessage

async def save_chat_history(message: ChatMessage):
    await db_helper.db.chat_history.insert_one(message.model_dump())

async def get_recent_history(user_id: str, limit: int = 10):
    cursor = db_helper.db.chat_history.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
    return await cursor.to_list(length=limit)