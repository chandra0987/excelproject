from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


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


@app.get("/", tags=["Health"])
def root():
    """Health-check endpoint."""
    return {"message": f"{settings.PROJECT_NAME} is running."}


@app.get("/health", tags=["Health"])
def health_check():
    """Health-check endpoint."""
    return {"status": "ok"}
