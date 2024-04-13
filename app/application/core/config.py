from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Настройки авторизации и аутентификации
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # БД
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str
    ECHO: bool = False

    REDIS_HOST: str
    REDIS_PORT: int
    EXPIRATION: int

    @property
    def database_url(self):
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_NAME,
        ).unicode_string()

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings: Settings = Settings()
