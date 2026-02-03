from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.interfaces import IRoleRepository
from src.infrastructure.models import Role, RolePermission
from src.presentation.schemas import RoleCreate, RoleUpdate


class RoleRepository(IRoleRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Optional[Role]:
        return self.session.query(Role).filter(Role.name == name).first()

    def get_by_id(self, role_id: UUID) -> Optional[Role]:
        return self.session.query(Role).filter(Role.id == role_id).first()

    def create(self, role: RoleCreate) -> Role:
        db_role = Role(name=role.name)
        self.session.add(db_role)
        self.session.commit()
        self.session.refresh(db_role)
        return db_role

    def update(self, role_model: Role, role: RoleUpdate) -> Role:
        update_data = role.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(role_model, field, value)
        self.session.commit()
        self.session.refresh(role_model)
        return role_model

    def delete(self, role: Role) -> None:
        self.session.delete(role)
        self.session.commit()

    def assign_permission(self, role_id: UUID, permission_id: UUID) -> bool:
        if self.session.query(RolePermission).filter_by(role_id=role_id, permission_id=permission_id).first():
            return False
        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        self.session.add(role_permission)
        self.session.commit()
        return True

    def revoke_permission(self, role_id: UUID, permission_id: UUID) -> bool:
        role_permission = self.session.query(RolePermission).filter_by(role_id=role_id,
                                                                       permission_id=permission_id).first()
        if not role_permission:
            return False
        self.session.delete(role_permission)
        self.session.commit()
        return True
