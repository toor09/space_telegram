import os
from pathlib import Path
from typing import List, Union

import requests


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
    _, _, image_filenames = [filename for filename in os.walk(path)][0]
    if not image_filenames:
        return []
    return image_filenames
