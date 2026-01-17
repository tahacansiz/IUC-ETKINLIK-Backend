from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.v1 import auth, event_api, user_api, event_participation_api, categories
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    # Import all models to register them with SQLAlchemy
    from app.models import user, event, category, event_participant, association_tables
    await init_db()
    print("✅ Database initialized successfully!")
    yield
    print("👋 Shutting down...")


app = FastAPI(title="IUC Event API", lifespan=lifespan)

# CORS middleware - allow Flutter app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth routes - /api/v1/auth/login, /api/v1/auth/register, etc.
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

# User routes - /api/v1/users/me, /api/v1/users/me/events/created, etc.
app.include_router(user_api.router, prefix="/api/v1", tags=["Users"])

# Event routes - /api/v1/events, /api/v1/events/{id}, etc.
app.include_router(event_api.router, prefix="/api/v1/events", tags=["Events"])

# Event participation routes - /api/v1/events/{id}/join, /api/v1/events/{id}/leave
app.include_router(event_participation_api.router, prefix="/api/v1", tags=["Event Participation"])

# Category routes - /api/v1/categories
app.include_router(categories.router, prefix="/api/v1", tags=["Categories"])

# Create media directory if it doesn't exist
os.makedirs("media", exist_ok=True)

# Static files for media/uploads
app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/")
async def root():
    return {"message": "IUC Event API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}