from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status, HTTPException

from src.common.enums import RoleTypes
from src.presentation.schemas import UserUpdate, RoleRead, RoleCreate, PermissionRead, PermissionCreate, UserRead
from src.common.security.dependencies import require_roles, require_permission
from src.core.services import UserService, RoleService, PermissionService

router = APIRouter(route_class=DishkaRoute,
                   dependencies=[Depends(require_roles([RoleTypes.ADMIN.value, RoleTypes.SUPER_ADMIN.value]))])


@router.get("/users")
def get_users(user_service: Annotated[UserService, FromDishka()]):
    return user_service.get_all_users()


@router.put("/users/{user_id}", dependencies=[Depends(require_permission("user.update"))])
def update_user(user_id: UUID, user: UserUpdate, user_service: Annotated[UserService, FromDishka()]):
    return user_service.update_user(user_id, user)


@router.delete("/users/{user_id}", dependencies=[Depends(require_permission("user.delete"))])
def delete_user(user_id: UUID, user_service: Annotated[UserService, FromDishka()]):
    user_service.delete_user(user_id)
    return {"status": "ok"}


@router.post("/role-create",
             response_model=RoleRead,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_permission("role.create"))]
             )
def create_role_with_permissions(role: RoleCreate, role_service: Annotated[RoleService, FromDishka()]):
    try:
        return role_service.create_role_with_permission(role, role.permission_ids)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/permission-create",
             response_model=PermissionRead,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_permission("permission.create"))]
             )
def create_permission(permission: PermissionCreate, permission_service: Annotated[PermissionService, FromDishka()]):
    try:
        return permission_service.create_permission(permission)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{user_id}/roles/{role_id}", response_model=UserRead)
def assign_role(user_id: UUID, role_id: UUID, user_service: Annotated[UserService, FromDishka()]):
    try:
        return user_service.assign_role(user_id, role_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
