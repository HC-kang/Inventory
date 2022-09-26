from typing import Optional

from pydantic import EmailStr, BaseModel, HttpUrl

from app.models.schemas.rwschema import RWSchema
from app.models.domain.users import User


class UserInLogin(RWSchema):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None


class UserWithToken(User):
    token: str


class UserInResponse(RWSchema):
    user: UserWithToken
