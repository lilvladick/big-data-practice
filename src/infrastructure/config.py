from pydantic_settings import BaseSettings, SettingsConfigDict

# я вшил все сюда, я плохой. мне лень везде создавать env для таких проектиков
class Settings(BaseSettings):
    SAKILA_DATABASE_URL: str = 'postgresql://sakila:p_ssW0rd@postgres-sakila:5432/sakila'
    AUTH_DATABASE_URL: str = 'postgresql://postgres:admin@postgres-auth:5432/auth_db'

    SPARK_JDBC_URL: str = "jdbc:postgresql://postgres-sakila:5432/sakila"
    SPARK_JDBC_USER: str = "sakila"
    SPARK_JDBC_PASSWORD: str = "p_ssW0rd"

    SECRET_KEY: str = 'super-secret'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_ignore_empty=True
    )


settings = Settings()
