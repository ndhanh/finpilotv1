from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    database_url: str

    # Security
    secret_key: str

    # CORS
    cors_origins: List[str]

    class Config:
        env_file = ".env"


settings = Settings()
