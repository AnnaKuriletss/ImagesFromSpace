import os
import argparse
import requests
from dotenv import load_dotenv
from utils import get_file_extension, download_image


def fetch_apod_images(folder_name, count, api_key):
    nasa_url = "https://api.nasa.gov/planetary/apod"

    params = {"api_key": api_key, "count": count}
    response = requests.get(nasa_url, params=params)
    response.raise_for_status()

    enasa_images_info = response.json()

    for index, image in enumerate(enasa_images_info):
        url = image.get("url")
        filename = f"nasa_apod_{index + 1}{get_file_extension(url)}"
        download_image(url, folder_name, filename)


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="Загрузка APOD NASA")
    parser.add_argument(
        "--count", type=int, default=5, help="Количество изображений для загрузки"
    )
    parser.add_argument(
        "--folder", type=str, default="images", help="Папка для сохранения фото"
    )
    args = parser.parse_args()

    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        raise ValueError("NASA_API_KEY не найден. Проверьте .env файл.")

    fetch_apod_images(args.folder, args.count, api_key)
