import os
import argparse
import requests
from datetime import datetime
from dotenv import load_dotenv
from utils import get_file_extension, downloading_images

load_dotenv()


def fetch_epic_images(folder_name, count, api_key):
    base_url = "https://epic.gsfc.nasa.gov/archive/natural"
    api_url = "https://api.nasa.gov/EPIC/api/natural/images"

    

    params = {"api_key": api_key}
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        images_data = response.json()

        if not images_data:
            print("Нет доступных изображений.")
            return

        selected_images = images_data[:count]

        for image_info in selected_images:
            image_date = image_info.get("date")
            image_name = image_info.get("image")

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
            downloading_images(image_url, folder_name, filename)

    except requests.RequestException as e:
        print(f"Ошибка загрузки EPIC NASA: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Загрузка EPIC NASA")
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

    fetch_epic_images(args.folder, args.count, api_key)
