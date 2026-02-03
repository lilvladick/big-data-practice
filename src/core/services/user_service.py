from typing import Optional, List
from uuid import UUID

from src.core.interfaces import IUserRepository, IRoleRepository
from src.presentation.schemas import UserCreate, UserRead, UserUpdate
from src.common.security import get_password_hash


class UserService:
    def __init__(self, user_repository: IUserRepository, role_repository: IRoleRepository):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def create_user(self, user: UserCreate) -> UserRead:
        if self.user_repository.get_by_email(user.email):
            raise ValueError('User with email already exists')

        hashed_password = get_password_hash(user.password)

        new_user = self.user_repository.create_user(
            UserCreate(
                first_name=user.first_name,
                last_name=user.last_name,
                patronymic=user.patronymic,
                email=user.email,
                password=hashed_password
            )
        )

        return UserRead(
            id=new_user.id,
            is_active=new_user.is_active,
            created_at=new_user.created_at
        )

    def get_user_by_id(self, user_id: UUID) -> Optional[UserRead]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None

        role_ids = [role.id for role in user.roles] if user.roles else []

        return UserRead(
            id=user.id,
            is_active=user.is_active,
            created_at=user.created_at,
            role_ids=role_ids
        )

    def get_user_by_email(self, email: str) -> Optional[UserRead]:
        user = self.user_repository.get_by_email(email)
        if not user:
            return None

        role_ids = [role.id for role in user.roles] if hasattr(user, "roles") else []

        return UserRead(
            id=user.id,
            is_active=user.is_active,
            created_at=user.created_at,
            role_ids=role_ids
        )

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserRead]:
        users = self.user_repository.get_all_users(skip, limit)
        return [
            UserRead(
                id=user.id,
                is_active=user.is_active,
                created_at=user.created_at,
                role_ids=[role.id for role in user.roles] if user.roles else []
            )
            for user in users
        ]

    def assign_role(self, user_id: UUID, role_id: UUID) -> UserRead:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('User does not exist')

        role = self.role_repository.get_by_id(role_id)
        if not role:
            raise ValueError('Role does not exist')

        new_role = self.user_repository.assign_role(user_id, role_id)
        if not new_role:
            raise ValueError('Role already assigned to user')
        role_ids = [role.id for role in user.roles] if user.roles else []

        return UserRead(
            id=user.id,
            is_active=user.is_active,
            created_at=user.created_at,
            role_ids=role_ids
        )

    def update_user(self, user_id: UUID, user_data: UserUpdate) -> Optional[UserRead]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None

        if user_data.password is not None:
            user_data.password = get_password_hash(user_data.password)

        updated_user = self.user_repository.update_user(user, user_data)
        role_ids = [role.id for role in updated_user.roles] if updated_user.roles else []

        return UserRead(
            id=updated_user.id,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
            role_ids=role_ids
        )

    def delete_user(self, user_id: UUID) -> bool:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False

        self.user_repository.delete_user(user)
        return True

    def revoke_role(self, user_id: UUID, role_id: UUID) -> UserRead:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('User does not exist')

        revoked = self.user_repository.revoke_role(user_id, role_id)
        if not revoked:
            raise ValueError('Role not assigned to user')

        user = self.user_repository.get_by_id(user_id)
        role_ids = [role.id for role in user.roles] if user.roles else []

        return UserRead(
            id=user.id,
            is_active=user.is_active,
            created_at=user.created_at,
            role_ids=role_ids
        )
