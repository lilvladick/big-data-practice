from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from src.presentation.schemas import LoginRequest, Token
from src.core.services import AuthService

router = APIRouter(route_class=DishkaRoute)


@router.post("/login", response_model=Token)
def login(login_schema: LoginRequest, auth_service: Annotated[AuthService, FromDishka()]):
    try:
        return auth_service.login(login_schema)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
