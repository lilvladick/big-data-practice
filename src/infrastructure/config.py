from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql://sakila:p_ssW0rd@localhost:5432/'
    AUTH_DATABASE: str = 'auth_db'
    SAKILA_DATABASE: str = 'sakila'
    SECRET_KEY: str = 'super-secret'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_ignore_empty=True
    )


settings = Settings()
