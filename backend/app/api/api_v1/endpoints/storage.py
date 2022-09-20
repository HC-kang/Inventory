import asyncio
from typing import Any, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.storage import (
    Storage,
    StorageCreate,
    StorageSearchResults,
    StorageSoftDelete,
    StorageUpdateRestricted,
)
from app.models.user import User

router = APIRouter()


@router.get("/{storage_id}", status_code=200)
async def fetch_storage(
    *,
    storage_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    storage = crud.storage.get(db=db, id=storage_id)
    if not storage:
        raise HTTPException(status_code=404, detail=f"{storage_id}번 저장소를 찾을 수 없습니다.")
    child_storages = crud.storage.get_by_parent(db=db, parent_id=storage_id)
    return {"results": {"main": storage, "children": child_storages}}
    return storage


@router.get("/my-storages/", status_code=200, response_model=StorageSearchResults)
async def fetch_user_storage(
    *,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    storages = current_user.storages
    if not storages:
        return {"storages": list()}
    return {"results": list(storages)}


@router.get("/search/", status_code=200, response_model=StorageSearchResults)
async def search_storage(
    *,
    keyword: str = Query(None),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    storages = crud.storage.get_multi(db=db, limit=max_results)
    results = filter(lambda x: keyword.lower() in x.name.lower(), storages)

    return {"results": list(results)}


@router.post("/", status_code=201, response_model=Storage)
async def create_storage(
    *,
    storage_in: StorageCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    if storage_in.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"오직 자신의 저장소만 등록 할 수 있습니다.")
    storage = crud.storage.create(db=db, obj_in=storage_in)

    return storage


@router.put("/", status_code=200, response_model=Storage)
async def update_storage(
    *,
    storage_in: StorageUpdateRestricted,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    storage = crud.storage.get(db, id=storage_in.id)
    if not storage:
        raise HTTPException(status_code=404, detail=f"{storage_in.id}번 저장소를 찾을 수 없습니다.")
    if storage.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"자신의 저장소 정보만 수정 할 수 있습니다.")

    updated_storage = crud.storage.update(db=db, db_obj=storage, obj_in=storage_in)
    return updated_storage


@router.delete("/{storage_id}", status_code=200, response_model=Storage)
async def delete_storage(
    *,
    storage_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    storage = crud.storage.get(db, id=storage_id)
    if not storage:
        raise HTTPException(status_code=404, detail=f"{storage_id}번 저장소를 찾을 수 없습니다.")
    if storage.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"자신의 저장소만 삭제 할 수 있습니다.")

    deleted_storage = crud.storage.soft_delete(db=db, db_obj=storage)
    return deleted_storage
