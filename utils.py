import os
from pathlib import Path
from typing import List, Union

import requests
from PIL import Image


def get_file_extension(url: str) -> str:
    """Return file extension for url."""
    return os.path.splitext(p=url)[-1]


def create_dirs(path: Union[Path, str]) -> None:
    """Create directories from path if not exists."""
    if not os.path.exists(path):
        os.makedirs(path)


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


def get_file_size(filename: Union[Path, str]) -> int:
    """Get filesize."""
    return os.stat(filename).st_size


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
