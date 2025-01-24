import logging

from dotenv import (
    load_dotenv,
)
from pydantic_settings import (
    BaseSettings,
)


logging.getLogger("passlib").setLevel(logging.ERROR)

load_dotenv()


class Settings(BaseSettings):
    postgres_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: int
    bot_token: str

    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
