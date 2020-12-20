from pydantic import BaseSettings


class Config(BaseSettings):
    SEARCH_API: str = "https://image.baidu.com/search/acjson"
    DOWNLOAD_API: str = "https://image.baidu.com/search/down"

    class Config:
        extra = "ignore"
