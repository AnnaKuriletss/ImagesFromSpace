import os
import argparse
import requests
from utils import get_file_extension, downloading_images


def fetch_spacex_images(folder_name, launch_id=None):

    spacex_url = (
        f"https://api.spacexdata.com/v5/launches/{launch_id}"
        if launch_id
        else "https://api.spacexdata.com/v5/launches/latest"
    )
    response = requests.get(spacex_url)
    response.raise_for_status()
    launch_record = response.json()

    photo_links = launch_record["links"].get("flickr", {}).get("original", [])

    if not photo_links:
        print("Нет фото для указанного запуска.")
        return

    for index, photo_url in enumerate(photo_links):
        filename = f"spacex_{index + 1}{get_file_extension(photo_url)}"
        downloading_images(photo_url, folder_name, filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Загрузка фото SpaceX")
    parser.add_argument(
        "--launch_id",
        type=str,
        help="ID запуска SpaceX. Если не указан, загружаются фото последнего запуска.",
    )
    parser.add_argument(
        "--folder", type=str, default="images", help="Папка для сохранения фото"
    )
    args = parser.parse_args()

    fetch_spacex_images(args.folder, args.launch_id)
