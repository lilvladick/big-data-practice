from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    permission_ids: List[UUID]


class RoleRead(RoleBase):
    id: UUID
    permission_ids: List[UUID] = []
    user_ids: List[UUID] = []

    model_config = ConfigDict(from_attributes=True)


class RoleUpdate(RoleBase):
    name: Optional[str] = None
