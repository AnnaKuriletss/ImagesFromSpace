import os
import argparse
import requests
from datetime import datetime
from dotenv import load_dotenv
from utils import download_image


def fetch_epic_images(folder_name, count, api_key):
    base_url = "https://epic.gsfc.nasa.gov/archive/natural"
    api_url = "https://api.nasa.gov/EPIC/api/natural/images"

    params = {"api_key": api_key}
    response = requests.get(api_url, params=params)
    response.raise_for_status()

    epic_images = response.json()

    if not epic_images:
        print("Нет доступных изображений.")
        return

    selected_images = epic_images[:count]

    for epic_image in selected_images:
        image_date = epic_image.get("date")
        image_name = epic_image.get("image")

        if not image_date or not image_name:
            print("Некорректные данные в ответе API.")
            continue

        try:
            date_obj = datetime.strptime(image_date, "%Y-%m-%d %H:%M:%S")
            formatted_date = date_obj.strftime("%Y/%m/%d")
        except ValueError:
            print(f"Некорректный формат даты: {image_date}")
            continue

        image_url = f"{base_url}/{formatted_date}/png/{image_name}.png"
        filename = f"epic_{image_name}.png"
        download_image(image_url, folder_name, filename)


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="Загрузка EPIC NASA")
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

    fetch_epic_images(args.folder, args.count, api_key)
