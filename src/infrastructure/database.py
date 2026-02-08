from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.config import settings

sakila_engine = create_engine(
    settings.SAKILA_DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    echo=False
)

auth_engine = create_engine(
    settings.AUTH_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo=False
)

SakilaSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sakila_engine)
AuthSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)
