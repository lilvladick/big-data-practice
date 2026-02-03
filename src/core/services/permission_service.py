from typing import Optional
from uuid import UUID

from src.core.interfaces import IPermissionRepository
from src.presentation.schemas import PermissionRead, PermissionCreate


class PermissionService:
    def __init__(self, permission_repository: IPermissionRepository):
        self.permission_repository = permission_repository

    def create_permission(self, permission: PermissionCreate) -> PermissionRead:
        existing_permission = self.permission_repository.get_by_name(permission.name)
        if existing_permission and existing_permission.resource == permission.resource:
            raise ValueError("Permission already exists for resource")

        new_permission = self.permission_repository.create(permission)

        return PermissionRead(
            id=new_permission.id,
            name=new_permission.name,
            resource=new_permission.resource
        )

    def get_permission_by_id(self, permission_id: UUID) -> Optional[PermissionRead]:
        permission = self.permission_repository.get_by_id(permission_id)
        if not permission:
            return None

        return PermissionRead(
            id=permission.id,
            name=permission.name,
            resource=permission.resource
        )

    def get_permission_by_name(self, permission_name: str) -> Optional[PermissionRead]:
        permission = self.permission_repository.get_by_name(permission_name)
        if not permission:
            return None

        return PermissionRead(
            id=permission.id,
            name=permission.name,
            resource=permission.resource
        )
