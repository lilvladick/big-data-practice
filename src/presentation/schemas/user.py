from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None = None
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(BaseModel):
    id: UUID
    is_active: bool
    created_at: datetime
    role_ids: List[UUID] = []

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    email: str | None = None
    is_active: bool | None = None
    password: str | None = None
