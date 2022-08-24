import time
from datetime import date, timedelta

import click
from requests import ConnectionError, HTTPError

from settings import NasaApiSettings, Settings
from utils import (
    correct_textwrap_dedent,
    create_dirs,
    get_file_extension,
    get_session,
    load_image,
    sanitize_file_path
)


@click.command()
@click.option(
    "-c", "--images-count",
    default=NasaApiSettings().NASA_APOD_IMAGES_COUNT,
    help="Images count for loading."
)
@click.option(
    "-w", "--is-last-week",
    default=False,
    help="Images published at last week."
)
def fetch_nasa_apod(images_count: int, is_last_week: bool) -> None:
    """Loading images from NASA API Astronomy Picture of the Day (APOD)."""
    settings = Settings()
    nasa_api_settings = NasaApiSettings()
    create_dirs(settings=settings)
    session = get_session(settings=settings)

    if is_last_week:
        apods = []
        current_date = date.today()
        end_date = date.today() - timedelta(days=7)
        while end_date != current_date:
            nasa_url_params = {
                "date": f"{current_date}",
                "api_key": nasa_api_settings.NASA_API_KEY,
            }
            apod = session.get(
                url="https://api.nasa.gov/planetary/apod",
                params=nasa_url_params,
                timeout=settings.TIMEOUT
            )
            apod.raise_for_status()
            apod = apod.json()
            current_date = current_date - timedelta(days=1)
            apods.append(apod)

    else:
        nasa_url_params = {
            "count": images_count,  # type: ignore
            "api_key": nasa_api_settings.NASA_API_KEY,
        }
        apods = session.get(
            url="https://api.nasa.gov/planetary/apod",
            params=nasa_url_params,
            timeout=settings.TIMEOUT
        )  # type: ignore
        apods.raise_for_status()  # type: ignore
        apods = apods.json()  # type: ignore

    for media_number, media_link in enumerate(apods, start=1):
        if media_link["media_type"] != "image":  # type: ignore
            continue
        image_link = media_link["url"]  # type: ignore
        file_name = "nasa_apod_"
        file_extension = get_file_extension(url=image_link)
        apod_nasa_path = sanitize_file_path(
            file_path=settings.IMG_PATH,
            file_name=f"{file_name}{media_number}{file_extension}"
        )
        try:
            load_image(url=str(image_link), file_path=apod_nasa_path)
            message = f"""{media_number})Фото по ссылке: {image_link!r}
                    было загружено по пути: {apod_nasa_path}
            """
            click.echo(message=correct_textwrap_dedent(message))

        except HTTPError as err:
            message = f"{media_number})Фото по ссылке: {image_link!r} " \
                        f"{err}"
            click.echo(message=message)

        except ConnectionError as err:
            message = f"Ошибка подключения :( {err}"
            click.echo(message=message)
            time.sleep(settings.TIMEOUT)


if __name__ == "__main__":
    fetch_nasa_apod()
