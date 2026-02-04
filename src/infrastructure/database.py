from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.config import settings

sakila_engine = create_engine(
    settings.DATABASE_URL+settings.SAKILA_DATABASE,
    pool_size=5,
    max_overflow=10,
    echo=False
)

auth_engine = create_engine(
    settings.DATABASE_URL+settings.AUTH_DATABASE,
    pool_size=10,
    max_overflow=20,
    echo=True
)

SakilaSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sakila_engine)
AuthSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)
