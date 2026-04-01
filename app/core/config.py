import os
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Manages app configuration using environment variables."""
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    DATABASE_NAME: str = "chatbot_db"

settings = Settings()

class DatabaseManager:
    """Handles the lifecycle of MongoDB and Redis connections."""
    def __init__(self):
        self.mongo_client: AsyncIOMotorClient = None
        self.db = None
        self.redis_client: redis.Redis = None

    async def connect(self):
        # Initialize MongoDB
        self.mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
        self.db = self.mongo_client[settings.DATABASE_NAME]
        
        # Initialize Redis
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        
        # Verify connections
        await self.redis_client.ping()
        print("Successfully connected to MongoDB and Redis!")

    async def close(self):
        if self.mongo_client:
            self.mongo_client.close()
        if self.redis_client:
            await self.redis_client.close()
        print("Database connections closed.")

# Single instance to be imported across the app
db_manager = DatabaseManager()