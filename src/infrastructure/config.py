from pydantic_settings import BaseSettings, SettingsConfigDict

# я вшил все сюда, я плохой. мне лень везде создавать env для таких проектиков
class Settings(BaseSettings):
    SAKILA_DATABASE_URL: str = 'postgresql://sakila:p_ssW0rd@localhost:5432/sakila'
    AUTH_DATABASE_URL: str = 'postgresql://postgres:admin@localhost:5434/auth_db'
    SECRET_KEY: str = 'super-secret'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_ignore_empty=True
    )


settings = Settings()
