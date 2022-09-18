from pydantic import BaseModel, HttpUrl

from typing import Sequence


class StorageBase(BaseModel):
    name: str


class StorageCreate(StorageBase):
    name: str
    user_id: int


class StorageUpdate(StorageBase):
    id: int


class StorageUpdateRestricted(BaseModel):
    id: int
    name: str


# Properties shared by models stored in DB
class StorageInDBBase(StorageBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Storage(StorageInDBBase):
    pass


# Properties properties stored in DB
class StorageInDB(StorageInDBBase):
    pass


class StorageSearchResults(BaseModel):
    results: Sequence[Storage]
