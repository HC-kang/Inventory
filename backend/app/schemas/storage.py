from datetime import datetime
from pydantic import BaseModel, HttpUrl

from typing import Optional, Sequence


class StorageBase(BaseModel):
    name: str


class StorageCreate(StorageBase):
    name: str
    user_id: int
    parent_id: Optional[int]


class StorageUpdate(StorageBase):
    id: int
    parent_id: Optional[int]


class StorageUpdateRestricted(BaseModel):
    id: int
    name: str


class StorageSoftDelete(BaseModel):
    id: int
    deleted_at: Optional[datetime]


# Properties shared by models stored in DB
class StorageInDBBase(StorageBase):
    id: int
    user_id: int
    parent_id: Optional[int]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


# Properties to return to client
class Storage(StorageInDBBase):
    pass


# Properties properties stored in DB
class StorageInDB(StorageInDBBase):
    pass


class StorageForService(StorageBase):
    name: str
    user_id: int
    parent_id: Optional[int]


class StorageSearchResults(BaseModel):
    results: Sequence[StorageForService]