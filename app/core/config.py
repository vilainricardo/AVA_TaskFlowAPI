from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    app_name: str = "TaskFlow API"
    api_v1_prefix: str = "/api/v1"
    environment: str = Field(default="local")
    sqlalchemy_echo: bool = False

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "taskflow"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    database_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url

        return str(
            URL.create(
                drivername="postgresql+psycopg",
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.postgres_port,
                database=self.postgres_db,
            )
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
