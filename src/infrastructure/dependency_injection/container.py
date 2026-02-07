from dishka import make_async_container

from src.infrastructure.dependency_injection.providers import RepositoryProvider, ServiceProvider

container = make_async_container(RepositoryProvider(), ServiceProvider())
