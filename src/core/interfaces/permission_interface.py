from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.infrastructure.models import Permission
from src.presentation.schemas import PermissionCreate, PermissionUpdate


class IPermissionRepository(ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Permission]:
        ...

    @abstractmethod
    def get_by_id(self, permission_id: UUID) -> Optional[Permission]:
        ...

    @abstractmethod
    def create(self, permission: PermissionCreate) -> Permission:
        ...

    @abstractmethod
    def update(self, permission_model: Permission, permission: PermissionUpdate) -> Permission:
        ...

    @abstractmethod
    def delete(self, permission: Permission) -> None:
        ...
