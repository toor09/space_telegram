import os
import textwrap
import time

import click
import requests
from pathvalidate import sanitize_filename, sanitize_filepath
from requests import ConnectionError, HTTPError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from settings import Settings
from utils import create_dirs, get_file_extension, load_image


@click.command()
@click.option(
    "-c", "--images-count",
    default=30,
    help="Images count for loading."
)
def fetch_nasa_apod(images_count: int) -> None:
    """Loading images from NASA API Astronomy Picture of the Day (APOD)."""
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
            apod_nasa_path = os.path.join(
                sanitize_filepath(settings.IMG_PATH),
                sanitize_filename(
                    f"{file_name}{image_number}{file_extension}"
                )
            )
            load_image(url=str(image_link), file_path=apod_nasa_path)
            message = f"""{image_number})Фото по ссылке: {image_link!r}
                    было загружено по пути: {apod_nasa_path}
            """
            message = "\n".join(
                [textwrap.dedent(line) for line in message.split("\n")]
            )
            click.echo(message)

        except HTTPError as exc:
            click.echo(f"{image_number})Фото по ссылке: {image_link!r} {exc}")

        except ConnectionError as exc:
            click.echo(f"Ошибка подключения :( {exc}")
            time.sleep(settings.TIMEOUT)


if __name__ == "__main__":
    fetch_nasa_apod()
