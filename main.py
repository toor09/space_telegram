import os
from datetime import datetime as dt
from pathlib import Path
from typing import Union

import requests
from pathvalidate import sanitize_filename, sanitize_filepath

from settings import Settings


def get_file_extension(url: str) -> str:
    """Return file extension for url."""
    return os.path.splitext(p=url)[-1]


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
        file_name = "space_x_"
        file_extension = ".jpg"
        image_space_x_path = os.path.join(
            sanitize_filepath(settings.IMG_PATH),
            sanitize_filename(f"{file_name}{image_number}{file_extension}")
        )
        load_image(url=str(image_url), file_path=image_space_x_path)


def fetch_nasa_apod(settings: Settings) -> None:
    """Loading images from NASA API Astronomy Picture of the Day (APOD)."""
    nasa_url = f"{settings.NASA_URL}{settings.NASA_URI_APOD}"
    nasa_url_params = {
        "count": settings.NASA_APOD_IMAGES_COUNT,
        "api_key": settings.NASA_API_KEY,
    }
    apod = requests.get(url=nasa_url, params=nasa_url_params)  # type: ignore
    apod.raise_for_status()

    for image_number, image_url in enumerate(apod.json(), start=1):
        image_link = image_url.get("url")
        file_name = "nasa_apod_"
        file_extension = get_file_extension(url=image_link)
        apod_nasa_path = os.path.join(
                sanitize_filepath(settings.IMG_PATH),
                sanitize_filename(f"{file_name}{image_number}{file_extension}")
            )
        load_image(url=str(image_link), file_path=apod_nasa_path)


def fetch_nasa_epic(settings: Settings) -> None:
    """
    Loading images from NASA API Earth Polychromatic Imaging Camera (EPIC).
    """
    nasa_url = f"{settings.NASA_URL}{settings.NASA_URI_EPIC}"
    nasa_url_params = {
        "api_key": settings.NASA_API_KEY,
    }
    epic = requests.get(url=nasa_url, params=nasa_url_params)
    epic.raise_for_status()
    epic_images = epic.json()

    epic_image_attrs = {}
    epic_images_attrs = []
    for epic_image in epic_images:
        epic_image_attrs["date"] = dt.fromisoformat(epic_image.get("date"))
        epic_image_attrs["image"] = epic_image.get("image")
        epic_images_attrs.append(epic_image_attrs)

    for image_number, image_url in enumerate(epic_images_attrs, start=1):
        file_name = "nasa_epic_"
        file_extension = ".png"
        image_creation_year = image_url["date"].year
        image_creation_month = f"0{image_url['date'].month}" if \
            image_url['date'].month < 10 else image_url['date'].month
        image_creation_day = image_url["date"].day
        image_name = image_url["image"]
        image_link = f"{settings.NASA_URL}{settings.NASA_URI_EPIC_ARCHIVE}/" \
                     f"{image_creation_year}/{image_creation_month}/" \
                     f"{image_creation_day}/png/{image_name}{file_extension}" \
                     f"?api_key={nasa_url_params.get('api_key')}"
        epic_nasa_path = os.path.join(
                sanitize_filepath(settings.IMG_PATH),
                sanitize_filename(f"{file_name}{image_number}{file_extension}")
            )
        load_image(url=str(image_link), file_path=epic_nasa_path)


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
    fetch_nasa_apod(settings=settings)
    fetch_nasa_epic(settings=settings)


if __name__ == "__main__":
    main()
