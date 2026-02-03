from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.infrastructure.models import Role
from src.presentation.schemas import RoleCreate, RoleUpdate


class IRoleRepository(ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Role]:
        ...

    @abstractmethod
    def get_by_id(self, role_id: UUID) -> Optional[Role]:
        ...

    @abstractmethod
    def create(self, role: RoleCreate) -> Role:
        ...

    @abstractmethod
    def update(self, role_model: Role, role: RoleUpdate) -> Role:
        ...

    @abstractmethod
    def delete(self, role: Role) -> None:
        ...

    @abstractmethod
    def assign_permission(self, role_id: UUID, permission_id: UUID) -> bool:
        ...

    @abstractmethod
    def revoke_permission(self, role_id: UUID, permission_id: UUID) -> bool:
        ...
