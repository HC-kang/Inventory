from fastapi import APIRouter, Body

from app.models.schemas.users import UserInLogin, UserInResponse

router = APIRouter()


@router.post("/login", response_model=UserInResponse, name="auth:login")
async def login(
    user_login: UserInLogin = Body(..., embed=True, alias="user"),
    # users_repo: UsersRepository
)