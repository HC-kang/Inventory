from datetime import datetime

from pydantic import BaseModel, validator, Field


class DateTimeModelMixin(BaseModel):
    created_at: datetime = None
    updated_at: datetime = None

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(
        cls,
        value: datetime,
    ) -> datetime:
        return value or datetime.now()


class IDModelMixin(BaseModel):
    id_: int = Field(0, alias="id")
