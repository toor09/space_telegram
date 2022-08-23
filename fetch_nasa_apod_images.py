import time

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
def fetch_nasa_apod(images_count: int) -> None:
    """Loading images from NASA API Astronomy Picture of the Day (APOD)."""
    settings = Settings()
    nasa_api_settings = NasaApiSettings()
    create_dirs(settings=settings)
    session = get_session(settings=settings)
    nasa_url_params = {
        "count": images_count,
        "api_key": nasa_api_settings.NASA_API_KEY,
    }
    apod = session.get(
        url="https://api.nasa.gov/planetary/apod",
        params=nasa_url_params,  # type: ignore
        timeout=settings.TIMEOUT
    )
    apod.raise_for_status()
    apod = apod.json()

    for media_number, media_link in enumerate(apod, start=1):
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
