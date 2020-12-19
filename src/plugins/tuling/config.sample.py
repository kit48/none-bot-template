from pydantic import BaseSettings


class Config(BaseSettings):
    API_KEY: str = "your key"

    class Config:
        extra = "ignore"
