from typing import Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.storage import Storage
from app.models.user import User
from app.schemas.storage import StorageCreate, StorageUpdateRestricted, StorageUpdate


class CRUDStorage(CRUDBase[Storage, StorageCreate, StorageUpdate]):
    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[StorageUpdate, StorageUpdateRestricted]
    ) -> Storage:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj


storage = CRUDStorage(Storage)
