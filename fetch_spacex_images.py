import sys
import time

import click
from requests import ConnectionError, HTTPError

from settings import Settings
from utils import (
    correct_textwrap_dedent,
    create_dirs,
    get_session,
    load_image,
    sanitize_file_path
)


@click.command()
@click.option(
    "-i", "--launch-id",
    default="latest",
    help="Lauch ID."
)
def fetch_spacex_last_launch(launch_id: str) -> None:
    """Loading images from SpaceX API last launch."""
    settings = Settings()
    create_dirs(settings=settings)
    session = get_session(settings=settings)
    space_x_images = session.get(
        url=f"https://api.spacexdata.com/v5/launches/{launch_id}",
        timeout=settings.TIMEOUT
    )
    space_x_images.raise_for_status()
    space_x_images = space_x_images.json()
    try:
        space_x_images = space_x_images[
            "links"
        ]["flickr"]["original"]  # type: ignore
    except KeyError:
        message = "Что-то не так с ответом от SpaceX API:("
        click.echo(message=message)
        sys.exit(1)

    for image_number, image_url in enumerate(space_x_images, start=1):
        file_name = "space_x_"
        file_extension = ".jpg"
        image_space_x_path = sanitize_file_path(
            file_path=settings.IMG_PATH,
            file_name=f"{file_name}{image_number}{file_extension}"
        )
        try:
            load_image(url=str(image_url), file_path=image_space_x_path)

            message = f"""{image_number})Фото по ссылке: {image_url!r}
                    было загружено по пути: {image_space_x_path}
            """
            click.echo(message=correct_textwrap_dedent(message))

        except HTTPError as err:
            message = f"{image_number})Фото по ссылке: {image_url!r} {err}"
            click.echo(message=message)

        except ConnectionError as err:
            message = f"Ошибка подключения :( {err}"
            click.echo(message=message)
            time.sleep(settings.TIMEOUT)


if __name__ == "__main__":
    fetch_spacex_last_launch()
