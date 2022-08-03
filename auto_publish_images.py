import os
import sys
import textwrap
import time
from random import shuffle

import click
import telegram
from pathvalidate import sanitize_filename, sanitize_filepath

from settings import Settings
from utils import (
    get_file_size,
    get_image_filenames,
    resize_image_file_to_limit
)


@click.command()
@click.option(
    "-t", "--publish-timeout",
    default=Settings().PUBLISH_IMAGE_TIMEOUT,
    help="Publish timeout in hours for auto posting."
)
def auto_publish_images(publish_timeout: int) -> None:
    """Auto publish images into Telegram channel."""
    settings = Settings()
    bot = telegram.Bot(token=settings.TG_BOT_TOKEN)

    while True:
        image_filenames = get_image_filenames(path=settings.IMG_PATH)
        if not image_filenames:
            click.echo(message="Фото для публикации не найдены...")
            sys.exit(1)

        shuffle(image_filenames)

        for image_filename in image_filenames:
            image_file_path = os.path.join(
                sanitize_filepath(
                    file_path=settings.IMG_PATH,
                    platform="auto"
                ),
                sanitize_filename(filename=image_filename, platform="auto")
            )
            if get_file_size(
                    filename=image_file_path
            ) > settings.TG_MAX_LIMIT_UPLOAD_FILE:
                resize_image_file_to_limit(
                    filename=image_file_path,
                    upload_limit=settings.TG_MAX_LIMIT_UPLOAD_FILE
                )
            bot.send_document(
                chat_id=settings.TG_CHAT_ID,
                document=open(file=image_file_path, mode="rb")
            )
            message = f"""Фото {image_file_path} было опубликовано в telegram
                    канале {settings.TG_CHAT_ID}.
            """
            message = "\n".join(
                [textwrap.dedent(line) for line in message.split("\n")]
            )
            click.echo(message=message)
        message = f"""Следующее обновление произойдет через
                {publish_timeout} ч.
        """
        message = "\n".join(
            [textwrap.dedent(line) for line in message.split("\n")]
        )
        click.echo(message=message)
        time.sleep(publish_timeout*60*60)


if __name__ == "__main__":
    auto_publish_images()
