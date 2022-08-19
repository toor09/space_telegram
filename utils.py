import os
import textwrap
from pathlib import Path
from typing import List, Union

import requests
from pathvalidate import sanitize_filename, sanitize_filepath
from PIL import Image
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from settings import Settings


def get_file_extension(url: str) -> str:
    """Return file extension for url."""
    return os.path.splitext(p=url)[-1]


def load_image(url: str, file_path: Union[Path, str]) -> None:
    """Loading image from URL."""
    image = requests.get(url=url)
    image.raise_for_status()

    with open(file_path, mode="wb") as file:
        file.write(image.content)


def get_image_filenames(path: Union[Path, str]) -> List[str]:
    """Get image filenames from directory."""
    try:
        _, _, image_filenames = [filename for filename in os.walk(path)][0]
    except IndexError:
        return []
    return image_filenames


def sanitize_file_path(file_path: Union[Path, str], file_name: str) -> str:
    """Sanitize file path."""
    sanitized_file_path = os.path.join(
        sanitize_filepath(file_path=file_path, platform="auto"),
        sanitize_filename(filename=file_name, platform="auto")
    )
    return sanitized_file_path


def get_file_size(filename: Union[Path, str]) -> int:
    """Get filesize."""
    return os.stat(filename).st_size


def correct_textwrap_dedent(multiline_message: str) -> str:
    """Correct textwrap dedent."""
    message = "\n".join(
        [
            textwrap.dedent(line_message)
            for line_message in multiline_message.split("\n")
        ]
    )
    return message


def resize_image_file_to_limit(
        filename: Union[Path, str],
        upload_limit: int
) -> None:
    """Resizing image under limits for Telegram upload."""
    with Image.open(fp=filename, mode="r") as source:
        quality = 100
        source.save(
            fp=filename,
            quality=quality,
            optimize=True,
            progressive=True
        )
        while get_file_size(filename=filename) >= upload_limit:
            source.save(
                fp=filename,
                quality=quality-1,
                optimize=True,
                progressive=True
            )
            quality -= 1


def create_dirs(settings: Settings) -> None:
    """Creates dirs for downloaded files."""
    images_path = sanitize_filepath(
        file_path=settings.IMG_PATH,
        platform="auto"
    )
    os.makedirs(name=images_path, exist_ok=True)


def get_session(
        settings: Settings
) -> requests.Session:
    """Get new request session with retry strategy."""
    retry_strategy = Retry(
        total=settings.RETRY_COUNT,
        status_forcelist=settings.STATUS_FORCE_LIST,
        allowed_methods=settings.ALLOWED_METHODS
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session
