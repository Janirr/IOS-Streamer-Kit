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


def get_resized_img(img_path, video_size):
    img = Image.open(img_path)
    width, height = video_size  # these are the MAX dimensions
    scale = width / height
    img_ratio = img.size[0] / img.size[1]
    if scale >= 1:
        if img_ratio <= scale:  # image is not wide enough
            width_new = int(height * img_ratio)
            size_new = width_new, height
        else:  # image is wider than video
            height_new = int(width / img_ratio)
            size_new = width, height_new
    else:
        if img_ratio >= scale:  # image is not tall enough
            height_new = int(width / img_ratio)
            size_new = width, height_new
        else:  # image is taller than video
            width_new = int(height * img_ratio)
            size_new = width_new, height
    return img.resize(size_new, resample=Image.LANCZOS)


def download_logos(match_json):
    path_general = os.path.abspath("")[:-7]
    # Path to download logos of the teams
    logo_home = match_json["teamHome"]['badgeImage']['mediumUrl']
    logo_away = match_json["teamAway"]['badgeImage']['mediumUrl']
    # Path where to put the files
    destination_home = path_general + "/teams/teamHome.png"
    destination_away = path_general + "/teams/teamAway.png"
    # Download them from their url and place them in the C:/Streamer kit/teams
    download(logo_home, "C:/Streamer kit/teams")
    download(logo_away, "C:/Streamer kit/teams")
    # Get name of the files by looking at the destination starting from the right
    home_logo_name = logo_home.split("/")[-1]
    away_logo_name = logo_away.split("/")[-1]
    # Full path to the downloaded logos (example: C:/Streamer kit/teams/1656.png)
    src_home = path_general + "/teams/" + home_logo_name
    src_away = path_general + "/teams/" + away_logo_name
    # Copy the file with different names: TeamHome.png and TeamAway.png
    shutil.copyfile(src_home, destination_home)
    shutil.copyfile(src_away, destination_away)
    # Resize Image Home into 256x256px
    size = 256, 256
    im = get_resized_img(destination_home, size)
    im.save(path_general + '/teams/' + 'teamHome.png')
    # Resize Image Away into 256x256px
    im2 = get_resized_img(destination_away, size)
    im2.save(path_general + '/teams/' + 'teamAway.png')