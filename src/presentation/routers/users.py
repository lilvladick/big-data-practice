from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from src.common.security.dependencies import get_current_user
from src.core.services import UserService
from src.presentation.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(route_class=DishkaRoute)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, user_service: Annotated[UserService, FromDishka()]):
    try:
        return user_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/delete")
def delete_current_user(user_service: Annotated[UserService, FromDishka()],
                        current_user: dict = Depends(get_current_user)):
    user_service.delete_user(UUID(current_user.get("id")))
    return {"status": "ok", "message": "User deleted successfully"}


@router.put("/update", response_model=UserRead)
def update_current_user(user_model: UserUpdate, user_service: Annotated[UserService, FromDishka()],
                        current_user: dict = Depends(get_current_user)):
    try:
        updated_user = user_service.update_user(UUID(current_user.get("id")), user_model)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
