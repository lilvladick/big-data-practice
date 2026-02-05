from dishka import make_async_container

from src.infrastructure.dependency_injection.providers import SQLAlchemyProvider, ServiceProvider

container = make_async_container(SQLAlchemyProvider(), ServiceProvider())
