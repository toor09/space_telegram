from pathlib import Path
from typing import List

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    IMG_PATH: Path = Path("images")
    NASA_API_KEY: str
    NASA_APOD_IMAGES_COUNT: int = 30
    TIMEOUT: int = 10
    RETRY_COUNT: int = 5
    STATUS_FORCE_LIST: str = "429,500,502,503,504"
    ALLOWED_METHODS: str = "HEAD,GET,OPTIONS"
    TG_BOT_TOKEN: str
    TG_CHAT_ID: str
    TG_MAX_LIMIT_UPLOAD_FILE: int = 10000000
    PUBLISH_IMAGE_TIMEOUT: int = 4

    @validator("STATUS_FORCE_LIST")
    def status_force_list(cls, v: str) -> List[int]:
        if isinstance(v, str):
            return [int(_v.strip()) for _v in v.split(",")]

    @validator("ALLOWED_METHODS")
    def allowed_methods(cls, v: str) -> List[str]:
        if isinstance(v, str):
            return [_v.strip() for _v in v.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True
