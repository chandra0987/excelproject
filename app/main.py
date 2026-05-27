from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.config import settings
from app.database import init_db, close_db
from app.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize MongoDB connection on startup and close on shutdown."""
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

# --- CORS ---
# Allow all origins during development; tighten in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse, include_in_schema=False, tags=["Frontend"])
def serve_frontend():
    """Serve the signup/login frontend."""
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/health", tags=["Health"])
def health_check():
    """Health-check endpoint."""
    return {"status": "ok"}
