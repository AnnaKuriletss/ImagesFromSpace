import os
import argparse
import requests
from dotenv import load_dotenv
from utils import get_file_extension, downloading_images


def fetch_apod_images(folder_name, count, api_key):
    nasa_url = "https://api.nasa.gov/planetary/apod"

    params = {"api_key": api_key, "count": count}
    try:
        response = requests.get(nasa_url, params=params)
        response.raise_for_status()

        images_data = response.json()

        for index, image in enumerate(images_data):
            url = image.get("url")
            filename = f"nasa_apod_{index + 1}{get_file_extension(url)}"
            downloading_images(url, folder_name, filename)

    except requests.RequestException as e:
        print(f"Ошибка загрузки APOD NASA: {e}")


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

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY не найден. Проверьте .env файл.")

    fetch_apod_images(args.folder, args.count, api_key)
