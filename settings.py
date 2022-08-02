from pathlib import Path
from typing import List

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    IMG_PATH: Path = Path("images")
    SPACE_X_URL: AnyHttpUrl
    SPACE_X_URI_LATEST: str
    SPACE_X_URI_LAUNCH_ID: str
    NASA_API_KEY: str
    NASA_URL: AnyHttpUrl
    NASA_URI_APOD: str
    NASA_URI_EPIC: str
    NASA_URI_EPIC_ARCHIVE: str
    TIMEOUT: int = 10
    RETRY_COUNT: int = 5
    STATUS_FORCE_LIST: str = "429,500,502,503,504"
    ALLOWED_METHODS: str = "HEAD,GET,OPTIONS"

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
