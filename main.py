import os
from pathlib import Path
from typing import Union

import requests
from pathvalidate import sanitize_filename, sanitize_filepath

from settings import Settings


def create_dirs(path: Union[Path, str]) -> None:
    """Create directories from path if not exists."""
    if not os.path.exists(path):
        os.makedirs(path)


def load_image(url: str, file_path: Union[Path, str]) -> None:
    """Loading image from URL."""
    image = requests.get(url=url)
    image.raise_for_status()

    with open(file_path, mode="wb") as file:
        file.write(image.content)


def main() -> None:
    """Main entry point."""
    settings = Settings()
    create_dirs(settings.IMG_PATH)
    image_path = os.path.join(
        sanitize_filepath(settings.IMG_PATH),
        sanitize_filename(settings.HUBBLE_PHOTO_FILE_NAME)
    )
    load_image(url=settings.HUBBLE_PHOTO_URL, file_path=image_path)


if __name__ == "__main__":
    main()
