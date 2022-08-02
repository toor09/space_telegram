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
from utils import create_dirs, load_image


@click.command()
@click.option(
    "-i", "--launch-id",
    default="latest",
    help="Id's Lauch."
)
def fetch_spacex_last_launch(launch_id: str) -> None:
    """Loading images from SpaceX API last launch."""
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

    space_x_url = f"{settings.SPACE_X_URL}{settings.SPACE_X_URI_LATEST}"\
        if launch_id == "latest" \
        else f"{settings.SPACE_X_URL}{settings.SPACE_X_URI_LAUNCH_ID}" \
             f"{launch_id}"

    space_x_images = session.get(url=space_x_url, timeout=settings.TIMEOUT)
    space_x_images.raise_for_status()

    space_x_images = space_x_images.json().get(
        "links"
    ).get("flickr").get("original")

    for image_number, image_url in enumerate(space_x_images, start=1):
        try:
            file_name = "space_x_"
            file_extension = ".jpg"
            image_space_x_path = os.path.join(
                sanitize_filepath(settings.IMG_PATH),
                sanitize_filename(f"{file_name}{image_number}{file_extension}")
            )
            load_image(url=str(image_url), file_path=image_space_x_path)

            message = f"""{image_number})Фото по ссылке: {image_url!r}
                    было загружено по пути: {image_space_x_path}
            """
            message = "\n".join(
                [textwrap.dedent(line) for line in message.split("\n")]
            )
            click.echo(message)

        except HTTPError as exc:
            click.echo(f"{image_number})Фото по ссылке: {image_url!r} {exc}")

        except ConnectionError as exc:
            click.echo(f"Ошибка подключения :( {exc}")
            time.sleep(settings.TIMEOUT)


if __name__ == "__main__":
    fetch_spacex_last_launch()
