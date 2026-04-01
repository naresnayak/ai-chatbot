import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-2.5-flash"  
        self.system_instruction = """
                                    You are the BITE BYTE assistant. 
                                    CRITICAL RULES:
                                    1. Be extremely concise. No introductory filler like 'Namaste' or 'I am thrilled'.
                                    2. Use bullet points only. 
                                    3. No bold headers or long descriptions unless asked.
                                    4. If a user asks for food options, provide a simple list.
                                    5. If a user asks for a recipe, provide a 'Crisp Recipe' format:
                                        - Ingredients (bullet points)
                                        - Quick Steps (numbered list)
                                        - Pro-Tip (one sentence)
                                    6. Always end with a question to keep the conversation going.
                                    CRITICAL: Keep responses under 200 words. No chatty introductions. Stay professional and food-focused.
                                    """
    def _formatted_history(self, chat_history: list):
        """Maps DB objects to Gemini types.Content objects."""
        formatted = []
        for msg in chat_history:
            # Determine role: 'model' is used instead of 'assistant' in Gemini
            role = "model" if msg.get("role") in ["assistant", "model"] else "user"
            
            # Map 'content' (from DB) to 'parts' (Gemini SDK)
            text_content = msg.get("content") or ""
            
            formatted.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=text_content)]
                )
            )
        return formatted
    async def stream_response(self, chat_history: list, user_message: str):
        # Use the stream=True equivalent in the SDK
        chat = self.client.aio.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.1,
                max_output_tokens=2000
            ),
            
            history=self._formatted_history(chat_history)
        )
        # This returns an iterable generator
        response_stream =  chat.send_message_stream(user_message)
        async for chunk in response_stream:
            if chunk.text:
                yield chunk.text
            
    async def generate_response(self, chat_history: list, user_message: str):
        # Create a chat session with existing history
        # Gemini expects a list of 'Content' objects (user/model roles)
        chat = self.client.aio.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.1,
                max_output_tokens=2000
            ),
           history=self._formatted_history(chat_history)
        )
        
        response = await chat.send_message(user_message)
        return response.text