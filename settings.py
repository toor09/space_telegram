from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    IMG_PATH: Path = Path("images")
    HUBBLE_PHOTO_URL: AnyHttpUrl
    HUBBLE_PHOTO_FILE_NAME: str
    SPACE_X_URL: AnyHttpUrl
    SPACE_X_URI_LATEST: str
    NASA_API_KEY: str
    NASA_URL: AnyHttpUrl
    NASA_URI_APOD: str
    NASA_URI_EPIC: str
    NASA_URI_EPIC_ARCHIVE: str
    NASA_APOD_IMAGES_COUNT: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True
