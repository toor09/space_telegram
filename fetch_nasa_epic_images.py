import time
from datetime import datetime as dt

import click
from requests import ConnectionError, HTTPError

from settings import Settings
from utils import (
    correct_textwrap_dedent,
    load_image,
    prepare_script_environment,
    sanitize_file_path
)


@click.command()
def fetch_nasa_epic() -> None:
    """
    Loading images from NASA API Earth Polychromatic Imaging Camera (EPIC).
    """
    session, settings = prepare_script_environment(settings=Settings())
    nasa_url_params = {
        "api_key": settings.NASA_API_KEY,
    }
    epic = session.get(
        url="https://api.nasa.gov/EPIC/api/natural/images",
        params=nasa_url_params,
        timeout=settings.TIMEOUT
    )
    epic.raise_for_status()
    epic_images = epic.json()

    epic_image_attrs = {}
    epic_images_attrs = []
    for epic_image in epic_images:
        epic_image_attrs["date"] = dt.fromisoformat(epic_image["date"])
        epic_image_attrs["image"] = epic_image["image"]
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
            image_link = f"https://api.nasa.gov/EPIC/archive/natural/" \
                         f"{image_creation_year}/{image_creation_month}/" \
                         f"{image_creation_day}/png/" \
                         f"{image_name}{file_extension}" \
                         f"?api_key={nasa_url_params['api_key']}"
            epic_nasa_path = sanitize_file_path(
                file_path=settings.IMG_PATH,
                file_name=f"{file_name}{image_number}{file_extension}"
            )
            load_image(url=str(image_link), file_path=epic_nasa_path)

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
