import sys
from random import choice
from typing import Optional

import click
import telegram

from settings import Settings, TelegramBotSettings
from utils import (
    correct_textwrap_dedent,
    get_file_size,
    get_image_filenames,
    resize_image_file_to_limit,
    sanitize_file_path
)


@click.command()
@click.option(
    "-f", "--image-filename",
    default=None,
    help="Image filename for publish."
)
def publish_images(image_filename: Optional[str]) -> None:
    """Publish text message to telegram channel."""
    settings = Settings()
    tg_bot_settings = TelegramBotSettings()
    bot = telegram.Bot(token=tg_bot_settings.TG_BOT_TOKEN)
    if image_filename:
        image_file_path = sanitize_file_path(
            file_path=settings.IMG_PATH,
            file_name=image_filename
        )
    else:
        image_filenames = get_image_filenames(path=settings.IMG_PATH)

        if not image_filenames:
            click.echo(message="Фото для публикации не найдены...")
            sys.exit(1)

        random_image_filename = choice(image_filenames)
        image_file_path = sanitize_file_path(
            file_path=settings.IMG_PATH,
            file_name=random_image_filename
        )
    try:
        if get_file_size(
            filename=image_file_path
        ) > tg_bot_settings.TG_MAX_LIMIT_UPLOAD_FILE:
            resize_image_file_to_limit(
                filename=image_file_path,
                upload_limit=tg_bot_settings.TG_MAX_LIMIT_UPLOAD_FILE
            )

        with open(file=image_file_path, mode="rb") as file:
            bot.send_document(
                chat_id=tg_bot_settings.TG_CHAT_ID,
                document=file,
            )
        message = f"""Фото {image_file_path} было опубликовано в telegram
                    канале {tg_bot_settings.TG_CHAT_ID}.
            """
        click.echo(message=correct_textwrap_dedent(message))

    except telegram.error.NetworkError as err:
        message = f"""Фото {image_file_path} не удалось опубликовать по
                причине: {err}.
        """
        click.echo(message=correct_textwrap_dedent(message))

    except FileNotFoundError as err:
        message = f"Фото не было опубликовано по причине {err}."
        click.echo(message=message)
        sys.exit(1)


if __name__ == "__main__":
    publish_images()
