from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.interfaces import IPermissionRepository
from src.infrastructure.models import Permission
from src.presentation.schemas import PermissionCreate, PermissionUpdate


class PermissionRepository(IPermissionRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Optional[Permission]:
        return self.session.query(Permission).filter(Permission.name == name).first()

    def get_by_id(self, permission_id: UUID) -> Optional[Permission]:
        return self.session.query(Permission).filter(Permission.id == permission_id).first()

    def create(self, permission: PermissionCreate) -> Permission:
        db_perm = Permission(name=permission.name, resource=permission.resource)
        self.session.add(db_perm)
        self.session.commit()
        self.session.refresh(db_perm)
        return db_perm

    def update(self, permission_model: Permission, permission: PermissionUpdate) -> Permission:
        update_data = permission.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(permission_model, field, value)
        self.session.commit()
        self.session.refresh(permission_model)
        return permission_model

    def delete(self, permission: Permission) -> None:
        self.session.delete(permission)
        self.session.commit()
