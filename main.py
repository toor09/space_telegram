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


def fetch_spacex_last_launch(settings: Settings) -> None:
    """Loading images from SpaceX API last launch."""
    space_x_url = f"{settings.SPACE_X_URL}{settings.SPACE_X_URI_LATEST}"
    space_x_images = requests.get(url=space_x_url)
    space_x_images.raise_for_status()

    space_x_images = space_x_images.json().get(
        "links"
    ).get("flickr").get("original")

    for image_number, image_url in enumerate(space_x_images, start=1):
        image_space_x_path = os.path.join(
            sanitize_filepath(settings.IMG_PATH),
            sanitize_filename(f"space_x_{image_number}.jpg")
        )
        load_image(url=str(image_url), file_path=image_space_x_path)


def main() -> None:
    """Main entry point."""
    settings = Settings()
    create_dirs(settings.IMG_PATH)
    image_path = os.path.join(
        sanitize_filepath(settings.IMG_PATH),
        sanitize_filename(settings.HUBBLE_PHOTO_FILE_NAME)
    )
    load_image(url=settings.HUBBLE_PHOTO_URL, file_path=image_path)

    fetch_spacex_last_launch(settings=settings)


if __name__ == "__main__":
    main()
