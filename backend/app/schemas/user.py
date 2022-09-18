from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.enums.user_approve_status_flag import UserApproveStatusFlag


class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    phone: Optional[str] = None
    level: int = 1
    point: int = 0
    business_class: Optional[str] = None
    business_name: Optional[str] = None
    business_president: Optional[str] = None
    is_notification: bool = False

    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    id: int


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    hashed_password: str
    approve_status_flag: Enum = UserApproveStatusFlag.W
    created_at: datetime
    updated_at: datetime


# Additional properties to return via API
class User(UserInDBBase):
    ...
