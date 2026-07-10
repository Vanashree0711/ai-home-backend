from fastapi import APIRouter
from app.api.v1 import auth, engine, chat, projects

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(engine.router, prefix="/engine", tags=["engine"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
