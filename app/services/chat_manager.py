from bson import ObjectId
from app.core.config import db_manager
from datetime import datetime
import json


class MongoJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle MongoDB ObjectIds and Datetimes automatically."""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            # Converts the date to an ISO format string (e.g., "2026-03-31T20:33:33")
            return obj.isoformat()
        return super().default(obj)

class ChatManager:
    async def get_history(self, session_id: str):
        # 1. Try Redis first
        context = await db_manager.redis_client.get(f"chat:{session_id}")
        if context:
            return json.loads(context)
        
        # 2. Fallback to Mongo
        # We sort by timestamp to ensure the conversation flow is correct
        history = await db_manager.db.chat_history.find(
            {"session_id": session_id}
        ).sort("timestamp", 1).to_list(10)
        
        return history

    async def update_history(self, session_id: str, role: str, content: str):
        # 1. Persist to MongoDB (Long-term storage)
        # We do this first to ensure the data is safe
        new_entry = {
            "session_id": session_id,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        await db_manager.db.chat_history.insert_one(new_entry)

        # 2. Update Redis (The "Pro Way" serialization)
        # Fetch current state, add new message, and dump using our custom encoder
        history = await self.get_history(session_id)
        history.append(new_entry)
        
        # 'cls=MongoJSONEncoder' handles the ObjectId conversion automatically!
        serialized_data = json.dumps(history[-5:], cls=MongoJSONEncoder)
        
        await db_manager.redis_client.setex(
            f"chat:{session_id}", 
            3600, 
            serialized_data
        )