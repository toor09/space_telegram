import time

import click
from requests import ConnectionError, HTTPError

from settings import Settings
from utils import (
    correct_textwrap_dedent,
    get_file_extension,
    load_image,
    prepare_script_environment,
    sanitize_file_path
)


@click.command()
@click.option(
    "-c", "--images-count",
    default=Settings().NASA_APOD_IMAGES_COUNT,
    help="Images count for loading."
)
def fetch_nasa_apod(images_count: int) -> None:
    """Loading images from NASA API Astronomy Picture of the Day (APOD)."""
    session, settings = prepare_script_environment(settings=Settings())
    nasa_url = f"{settings.NASA_URL}{settings.NASA_URI_APOD}"
    nasa_url_params = {
        "count": images_count,
        "api_key": settings.NASA_API_KEY,
    }
    apod = session.get(
        url=nasa_url,
        params=nasa_url_params,  # type: ignore
        timeout=settings.TIMEOUT
    )
    apod.raise_for_status()

    for image_number, image_url in enumerate(apod.json(), start=1):
        try:
            image_link = image_url.get("url")
            file_name = "nasa_apod_"
            file_extension = get_file_extension(url=image_link)
            apod_nasa_path = sanitize_file_path(
                file_path=settings.IMG_PATH,
                file_name=f"{file_name}{image_number}{file_extension}"
            )
            load_image(url=str(image_link), file_path=apod_nasa_path)
            message = f"""{image_number})Фото по ссылке: {image_link!r}
                    было загружено по пути: {apod_nasa_path}
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
    fetch_nasa_apod()
