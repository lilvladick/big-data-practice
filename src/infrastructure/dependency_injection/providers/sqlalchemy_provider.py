from typing import Iterator

from dishka import Provider, Scope, provide
from sqlalchemy.orm import Session

from src.infrastructure.database import AuthSessionLocal
from src.core.interfaces import IUserRepository, IRoleRepository, IPermissionRepository
from src.infrastructure.repositories import UserRepository, PermissionRepository, RoleRepository


class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_session(self) -> Iterator[Session]:
        session = AuthSessionLocal()
        try:
            yield session
        finally:
            session.close()

    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: Session) -> IUserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_role_repository(self, session: Session) -> IRoleRepository:
        return RoleRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_permission_repository(self, session: Session) -> IPermissionRepository:
        return PermissionRepository(session)
