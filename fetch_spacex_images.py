import sys
import time

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
@click.option(
    "-i", "--launch-id",
    default="latest",
    help="Lauch ID."
)
def fetch_spacex_last_launch(launch_id: str) -> None:
    """Loading images from SpaceX API last launch."""
    session, settings = prepare_script_environment(settings=Settings())
    space_x_url = f"{settings.SPACE_X_URL}{settings.SPACE_X_URI_LATEST}"\
        if launch_id == "latest" \
        else f"{settings.SPACE_X_URL}{settings.SPACE_X_URI_LAUNCH_ID}" \
             f"{launch_id}"

    space_x_images = session.get(url=space_x_url, timeout=settings.TIMEOUT)
    space_x_images.raise_for_status()
    try:
        space_x_images = space_x_images.json()["links"]["flickr"]["original"]
    except KeyError:
        message = "Что-то не так с ответом от стороннего API:("
        click.echo(message=message)
        sys.exit(1)

    for image_number, image_url in enumerate(space_x_images, start=1):
        try:
            file_name = "space_x_"
            file_extension = ".jpg"
            image_space_x_path = sanitize_file_path(
                file_path=settings.IMG_PATH,
                file_name=f"{file_name}{image_number}{file_extension}"
            )
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
