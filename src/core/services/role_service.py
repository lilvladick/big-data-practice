from typing import List, Optional
from uuid import UUID

from src.core.interfaces import IRoleRepository, IPermissionRepository
from src.presentation.schemas import RoleCreate, RoleRead


class RoleService:
    def __init__(self, role_repository: IRoleRepository, permission_repository: IPermissionRepository):
        self.role_repository = role_repository
        self.permission_repository = permission_repository

    def create_role_with_permission(self, role: RoleCreate, permission_ids: List[UUID]) -> RoleRead:
        if self.role_repository.get_by_name(role.name):
            raise Exception('Role already exists')

        new_role = self.role_repository.create(role)

        for permission_id in permission_ids:
            self.role_repository.assign_permission(new_role.id, permission_id)

        return RoleRead(
            id=new_role.id,
            name=new_role.name,
            permission_ids=[permission.id for permission in new_role.permissions]
        )

    def get_role_by_name(self, name: str) -> Optional[RoleRead]:
        role = self.role_repository.get_by_name(name)
        if not role:
            return None

        return RoleRead(
            id=role.id,
            name=role.name,
            permission_ids=[p.id for p in role.permissions],
            user_ids=[u.id for u in role.users] if role.users else []
        )

    def get_role_by_id(self, role_id: UUID) -> Optional[RoleRead]:
        role = self.role_repository.get_by_id(role_id)
        if not role:
            return None

        return RoleRead(
            id=role.id,
            name=role.name,
            permission_ids=[p.id for p in role.permissions],
            user_ids=[u.id for u in role.users] if role.users else []
        )
