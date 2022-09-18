from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app import crud
from app import schemas
from app.api import deps
from app.core.auth import (
    authenticate,
    create_access_token,
)
from app.models.user import User

router = APIRouter()


@router.post("/login")
async def login(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 리퀘스트로 개인의 JWT 토큰을 발행합니다.
    """

    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="유저 정보를 확인 할 수 없습니다.")

    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: User = Depends(deps.get_current_user)):
    """
    현재 로그인한 유저의 정보를 가져옵니다.
    """

    user = current_user
    return user


@router.post("/signup", response_model=schemas.User, status_code=201)
async def create_user_signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
) -> Any:
    """
    새로운 유저를 생성합니다.
    """

    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="이미 사용중인 이메일입니다.",
        )
    user = crud.user.create(db=db, obj_in=user_in)

    return user


@router.put("/me", status_code=200, response_model=schemas.User)
async def update_user(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    user_in: schemas.user.UserUpdate,
) -> Any:

    user = crud.user.get(db, id=user_in.id)

    if not user:
        raise HTTPException(status_code=404, detail="해당하는 유저를 찾을 수 없습니다.")
    if not current_user.id == user.id:
        raise HTTPException(status_code=403, detail="본인의 계정 정보만 수정 할 수 있습니다.")

    updated_user = crud.user.update(db=db, db_obj=user, obj_in=user_in)

    return updated_user