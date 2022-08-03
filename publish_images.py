import os
import sys
import textwrap
from random import choice
from typing import Optional

import click
import telegram
from pathvalidate import sanitize_filename, sanitize_filepath

from settings import Settings
from utils import get_image_filenames


@click.command()
@click.option(
    "-f", "--image-filename",
    default=None,
    help="Image filename for publish."
)
def publish_images(image_filename: Optional[str]) -> None:
    """Publish text message to telegram channel."""
    settings = Settings()
    bot = telegram.Bot(token=settings.TG_BOT_TOKEN)
    if image_filename:
        image_file_path = os.path.join(
            sanitize_filepath(file_path=settings.IMG_PATH, platform="auto"),
            sanitize_filename(filename=image_filename, platform="auto")
        )
    else:
        image_filenames = get_image_filenames(path=settings.IMG_PATH)

        if not image_filenames:
            click.echo(message="Фото для публикации не найдены...")
            sys.exit(1)

        random_image_filename = choice(image_filenames)
        image_file_path = os.path.join(
            sanitize_filepath(file_path=settings.IMG_PATH, platform="auto"),
            sanitize_filename(filename=random_image_filename, platform="auto")
        )
    try:
        with open(file=image_file_path, mode="rb") as file:
            bot.send_document(
                chat_id=settings.TG_CHAT_ID,
                document=file,
            )
    except FileNotFoundError as err:
        click.echo(message=f"Фото не было опубликовано по причине {err}.")
        sys.exit(1)

    message = f"""{image_file_path} было опубликовано в telegram
            канале {settings.TG_CHAT_ID}.
    """
    message = "\n".join(
        [textwrap.dedent(line) for line in message.split("\n")]
    )
    click.echo(message=message)


if __name__ == "__main__":
    publish_images()
