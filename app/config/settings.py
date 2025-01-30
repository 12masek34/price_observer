import logging

from dotenv import (
    load_dotenv,
)
from pydantic_settings import (
    BaseSettings,
)


load_dotenv()
logging.getLogger("passlib").setLevel(logging.ERROR)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


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

OZON = "OZON"
WILDBERRIES = "WILDBERRIES"
DELETE_SUBSCRIPTION_PREFIX = "delete_subscription_"
DELAY_BY_PRICE_CHECK = 600
PARSE_RETRIES = 3
PARSE_TIMEOUT = 5
