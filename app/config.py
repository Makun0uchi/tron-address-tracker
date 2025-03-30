from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    tron_network: str = 'nile'

    class Config:
        env_file = Path(__file__).parent.parent / '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
