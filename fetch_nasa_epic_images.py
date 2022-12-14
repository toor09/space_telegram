import time
from datetime import datetime as dt

import click
from requests import ConnectionError, HTTPError

from settings import NasaApiSettings, Settings
from utils import (
    correct_textwrap_dedent,
    create_dirs,
    get_session,
    load_image,
    sanitize_file_path
)


@click.command()
def fetch_nasa_epic() -> None:
    """
    Loading images from NASA API Earth Polychromatic Imaging Camera (EPIC).
    """
    settings = Settings()
    nasa_api_settings = NasaApiSettings()
    create_dirs(settings=settings)
    session = get_session(settings=settings)
    nasa_url_params = {
        "api_key": nasa_api_settings.NASA_API_KEY,
    }
    epic = session.get(
        url="https://api.nasa.gov/EPIC/api/natural/images",
        params=nasa_url_params,
        timeout=settings.TIMEOUT
    )
    epic.raise_for_status()
    epic_images = epic.json()

    for image_number, image_url in enumerate(epic_images, start=1):
        file_name = "nasa_epic_"
        file_extension = ".png"
        image_name = image_url["image"]
        image_creation_date = f"{dt.fromisoformat(image_url['date']):%Y.%m.%d}"
        image_creation_year, image_creation_month, image_creation_day = \
            image_creation_date.split(".")
        image_link = f"https://api.nasa.gov/EPIC/archive/natural/" \
                     f"{image_creation_year}/{image_creation_month}/" \
                     f"{image_creation_day}/png/" \
                     f"{image_name}{file_extension}"
        epic_nasa_path = sanitize_file_path(
            file_path=settings.IMG_PATH,
            file_name=f"{file_name}{image_number}{file_extension}"
        )
        try:
            load_image(
                url=str(image_link),
                file_path=epic_nasa_path,
                params=nasa_url_params
            )
            message = f"""{image_number})Фото по ссылке: {image_link!r} было
                    загружено по пути: {epic_nasa_path}
            """
            click.echo(message=correct_textwrap_dedent(message))

        except HTTPError as err:
            message = f"{image_number})Фото по ссылке: {image_link!r} {err}"
            click.echo(message=message)

        except ConnectionError as err:
            message = f"Ошибка подключения :( {err}"
            click.echo(message=message)
            time.sleep(settings.TIMEOUT)


if __name__ == "__main__":
    fetch_nasa_epic()
