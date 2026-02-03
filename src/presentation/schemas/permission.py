from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PermissionBase(BaseModel):
    name: str
    resource: str


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class PermissionUpdate(PermissionBase):
    name: Optional[str] = None
    resource: Optional[str] = None
