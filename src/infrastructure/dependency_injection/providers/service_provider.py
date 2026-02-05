from dishka import Provider, Scope, provide

from src.core.interfaces import IUserRepository, IRoleRepository, IPermissionRepository
from src.core.services import UserService, RoleService, PermissionService, AuthService


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_service(self, user_repository: IUserRepository, role_repository: IRoleRepository) -> UserService:
        return UserService(user_repository, role_repository)

    @provide(scope=Scope.REQUEST)
    def get_role_service(self, role_repository: IRoleRepository,
                         permission_repository: IPermissionRepository) -> RoleService:
        return RoleService(role_repository, permission_repository)

    @provide(scope=Scope.REQUEST)
    def get_permission_service(self, permission_repository: IPermissionRepository) -> PermissionService:
        return PermissionService(permission_repository)

    @provide(scope=Scope.REQUEST)
    def get_auth_service(self, user_repository: IUserRepository,
                         permission_repository: IPermissionRepository) -> AuthService:
        return AuthService(user_repository, permission_repository)
