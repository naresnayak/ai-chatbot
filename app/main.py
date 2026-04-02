from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from app.core.config import db_manager
from app.routes import chat  # Import the new route
from fastapi.middleware.cors import CORSMiddleware

# Manage DB connections gracefully
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Open Mongo and Redis connections
    await db_manager.connect()
    yield
    # Shutdown: Close connections
    await db_manager.close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Session-ID"] # This must be present
)

templates = Jinja2Templates(directory="app/templates")

# Include the Chat Router
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """Serves the frontend homepage."""
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "title": "BITE BYTE Chat"
    })