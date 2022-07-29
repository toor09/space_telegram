from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    IMG_PATH: Path = Path("images")
    HUBBLE_PHOTO_URL: AnyHttpUrl
    HUBBLE_PHOTO_FILE_NAME: str

    class Config:
        env_file = ".env"
        case_sensitive = True
