import os
import time
from datetime import datetime as dt

import click
import requests
from pathvalidate import sanitize_filename, sanitize_filepath
from requests import ConnectionError, HTTPError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from settings import Settings
from utils import create_dirs, load_image


@click.command()
def fetch_nasa_epic() -> None:
    """
    Loading images from NASA API Earth Polychromatic Imaging Camera (EPIC).
    """
    settings = Settings()
    create_dirs(settings.IMG_PATH)
    retry_strategy = Retry(
        total=settings.RETRY_COUNT,
        status_forcelist=settings.STATUS_FORCE_LIST,
        allowed_methods=settings.ALLOWED_METHODS
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    nasa_url = f"{settings.NASA_URL}{settings.NASA_URI_EPIC}"
    nasa_url_params = {
        "api_key": settings.NASA_API_KEY,
    }
    epic = session.get(
        url=nasa_url,
        params=nasa_url_params,
        timeout=settings.TIMEOUT
    )
    epic.raise_for_status()
    epic_images = epic.json()

    epic_image_attrs = {}
    epic_images_attrs = []
    for epic_image in epic_images:
        epic_image_attrs["date"] = dt.fromisoformat(epic_image.get("date"))
        epic_image_attrs["image"] = epic_image.get("image")
        epic_images_attrs.append(epic_image_attrs)
        epic_image_attrs = {}
    for image_number, image_url in enumerate(epic_images_attrs, start=1):
        try:
            file_name = "nasa_epic_"
            file_extension = ".png"
            image_creation_year = image_url["date"].year
            image_creation_month = f"0{image_url['date'].month}" if \
                image_url['date'].month < 10 else image_url['date'].month
            image_creation_day = f"0{image_url['date'].day}" if \
                image_url['date'].day < 10 else image_url['date'].day
            image_name = image_url["image"]
            image_link = f"{settings.NASA_URL}" \
                         f"{settings.NASA_URI_EPIC_ARCHIVE}/" \
                         f"{image_creation_year}/{image_creation_month}/" \
                         f"{image_creation_day}/png/" \
                         f"{image_name}{file_extension}" \
                         f"?api_key={nasa_url_params.get('api_key')}"
            epic_nasa_path = os.path.join(
                sanitize_filepath(settings.IMG_PATH, platform="auto"),
                sanitize_filename(
                    f"{file_name}{image_number}{file_extension}"
                )
            )
            load_image(url=str(image_link), file_path=epic_nasa_path)

            message = f"{image_number})Фото по ссылке: {image_link!r} " \
                      f"было загружено по пути: {epic_nasa_path}"
            click.echo(message)

        except HTTPError as exc:
            click.echo(f"{image_number})Фото по ссылке: {image_link!r} {exc}")

        except ConnectionError as exc:
            click.echo(f"Ошибка подключения :( {exc}")
            time.sleep(settings.TIMEOUT)


if __name__ == "__main__":
    fetch_nasa_epic()
