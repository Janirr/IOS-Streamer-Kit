import os
import shutil
from typing import Tuple
from urllib.request import urlopen

from PIL import Image


def download(url: str, dest_folder: str) -> str:
    """Download a file from a URL to a folder."""
    os.makedirs(dest_folder, exist_ok=True)
    filename = os.path.basename(url).replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)

    with urlopen(url) as response, open(file_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    return file_path


def resize_image(img_path: str, size: Tuple[int, int]) -> Image:
    """Resize an image to fit the specified size."""
    with Image.open(img_path) as img:
        img.thumbnail(size, Image.LANCZOS)
        return img


def download_logos(match_json):
    path_general = os.path.abspath("")[:-7]
    # Path to download logos of the teams
    logo_home = match_json["teamHome"]['badgeImage']['mediumUrl']
    logo_away = match_json["teamAway"]['badgeImage']['mediumUrl']
    # Path where to put the files
    destination_home = os.path.join(path_general, "teams", "teamHome.png")
    destination_away = os.path.join(path_general, "teams", "teamAway.png")
    # Download them from their URL and place them in the C:/Streamer kit/teams
    download(logo_home, os.path.join(path_general, "teams"))
    download(logo_away, os.path.join(path_general, "teams"))
    # Resize Image Home into 256x256px
    resize_image(destination_home, (256, 256)).save(destination_home)
    # Resize Image Away into 256x256px
    resize_image(destination_away, (256, 256)).save(destination_away)