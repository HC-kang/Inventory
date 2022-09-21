from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, storage


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(storage.router, prefix="/storage", tags=["storage"])
