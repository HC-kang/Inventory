from fastapi import APIRouter

from app.api.routes.api_v1 import authentication

router = APIRouter()
router.include_router(authentication.router, tags=["authentication"], prefix="/users")
