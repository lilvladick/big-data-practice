from typing import Optional, List
from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from src.core.interfaces import IUserRepository
from src.infrastructure.models import User, UserRole, RolePermission, Permission
from src.presentation.schemas import UserCreate, UserUpdate


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.session.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate) -> User:
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            patronymic=user.patronymic,
            email=user.email,
            password_hash=user.password,
            is_active=True,
        )

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def update_user(self, user_model: User, user: UserUpdate) -> User:
        data = user.model_dump(exclude_unset=True)
        for key, value in data.items():
            if value is not None:
                setattr(user_model, key, value)

        self.session.add(user_model)
        self.session.commit()
        return user_model

    def delete_user(self, user: User) -> None:
        user.is_active = False
        self.session.commit()

    def assign_role(self, user_id: UUID, role_id: UUID) -> bool:
        existing = self.session.query(UserRole).filter_by(user_id=user_id, role_id=role_id).first()
        if existing:
            return False

        user_role = UserRole(user_id=user_id, role_id=role_id)
        self.session.add(user_role)
        self.session.commit()
        return True

    def revoke_role(self, user_id: UUID, role_id: UUID) -> bool:
        user_role = self.session.query(UserRole).filter_by(user_id=user_id, role_id=role_id).first()
        if not user_role:
            return False
        self.session.delete(user_role)
        self.session.commit()
        return True

    def check_permission(self, user_id: UUID, permission_name: str) -> bool:
        stmt = select(
            exists().where(
                UserRole.user_id == user_id,
                UserRole.role_id == RolePermission.role_id,
                RolePermission.permission_id == Permission.id,
                Permission.name == permission_name,
            )
        )
        return self.session.execute(stmt).scalar_one()
