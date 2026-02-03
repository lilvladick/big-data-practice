from src.core.interfaces import IUserRepository, IPermissionRepository
from src.presentation.schemas.auth import LoginRequest, Token
from src.common.security import verify_password, create_access_token


class AuthService:
    def __init__(self, user_repository: IUserRepository, permission_repository: IPermissionRepository):
        self.user_repository = user_repository
        self.permission_repository = permission_repository

    def login(self, login: LoginRequest):
        user = self.user_repository.get_by_email(login.email)
        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(login.password, user.password_hash):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User deactivated")

        roles = [role.name for role in user.roles] if user.roles else []

        permissions_names = set()
        for role in user.roles:
            for permission in role.permissions:
                permissions_names.add(permission.name)

        token_data = {"sub": str(user.id), "roles": roles, "permissions": list(permissions_names)}
        access_token = create_access_token(token_data)
        return Token(access_token=access_token)