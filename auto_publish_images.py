import sys
import time
from random import shuffle

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
    "-t", "--publish-timeout",
    default=Settings().PUBLISH_IMAGE_TIMEOUT,
    help="Publish timeout in hours for auto posting."
)
def auto_publish_images(publish_timeout: int) -> None:
    """Auto publish images into Telegram channel."""
    settings = Settings()
    tg_bot_settings = TelegramBotSettings()
    bot = telegram.Bot(token=tg_bot_settings.TG_BOT_TOKEN)

    while True:
        image_filenames = get_image_filenames(path=settings.IMG_PATH)
        if not image_filenames:
            click.echo(message="Фото для публикации не найдены...")
            sys.exit(1)

        shuffle(image_filenames)

        for image_filename in image_filenames:
            image_file_path = sanitize_file_path(
                file_path=settings.IMG_PATH,
                file_name=image_filename
            )
            if get_file_size(
                    filename=image_file_path
            ) > tg_bot_settings.TG_MAX_LIMIT_UPLOAD_FILE:
                resize_image_file_to_limit(
                    filename=image_file_path,
                    upload_limit=tg_bot_settings.TG_MAX_LIMIT_UPLOAD_FILE
                )
            try:
                bot.send_document(
                    chat_id=tg_bot_settings.TG_CHAT_ID,
                    document=open(file=image_file_path, mode="rb")
                )
                message = f"""Фото {image_file_path} было опубликовано в telegram
                        канале {tg_bot_settings.TG_CHAT_ID}.
                """
                click.echo(message=correct_textwrap_dedent(message))

            except telegram.error.NetworkError as err:
                message = f"""Фото {image_file_path} не удалось опубликовать
                        по причине: {err}.
                """
                click.echo(message=correct_textwrap_dedent(message))

            message = f"""Следующая публикация фото произойдет через
                    {publish_timeout} ч.
            """
            click.echo(message=correct_textwrap_dedent(message))
            time.sleep(publish_timeout*60*60)


if __name__ == "__main__":
    auto_publish_images()
