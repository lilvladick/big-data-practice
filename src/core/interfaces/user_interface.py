from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from src.infrastructure.models import User
from src.presentation.schemas import UserUpdate, UserCreate


class IUserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        ...

    @abstractmethod
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        ...

    @abstractmethod
    def create_user(self, user: UserCreate) -> User:
        ...

    @abstractmethod
    def update_user(self, user_model: User, user: UserUpdate) -> User:
        ...

    @abstractmethod
    def delete_user(self, user: User) -> None:
        ...

    @abstractmethod
    def assign_role(self, user_id: UUID, role_id: UUID) -> bool:
        ...

    @abstractmethod
    def revoke_role(self, user_id: UUID, role_id: UUID) -> bool:
        ...

    @abstractmethod
    def check_permission(self, user_id: UUID, permission_name: str) -> bool:
        ...
