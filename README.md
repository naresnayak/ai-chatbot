# 🍕 Bite Byte AI Chatbot

Bite Byte is a high-performance, conversational AI assistant designed for food enthusiasts. It provides concise recipes, food suggestions, and pro-tips using the Google Gemini API, with a robust backend architecture optimized for speed and persistence.

## 🚀 Features

- **AI Engine:** Powered by `gemini-2.0-flash` for near-instant responses.
- **Streaming Responses:** Real-time text generation for a smooth UI experience.
- **Dual-Layer Memory:**
    - **Redis:** In-memory caching for ultra-fast retrieval of active conversation context.
    - **MongoDB:** Permanent storage for long-term chat history.
- **Bite-Sized Logic:** Structured system instructions to ensure the bot stays concise and food-focused.
- **Pro Serialization:** Custom JSON encoding to handle MongoDB ObjectIds and Datetimes seamlessly.

## 🛠️ Tech Stack

- **Backend:** Python 3.11, FastAPI, Uvicorn
- **AI SDK:** Google GenAI Python SDK
- **Databases:** MongoDB (Motor driver), Redis (aioredis)
- **DevOps:** Docker, Docker Compose
- **Validation:** Pydantic v2

## 📋 Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose installed.
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey).

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/naresnayak/ai-chatbot.git](https://github.com/naresnayak/ai-chatbot.git)
   cd ai-chatbot