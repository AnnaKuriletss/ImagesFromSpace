import os
import requests
from urllib.parse import urlparse
from datetime import datetime
from dotenv import load_dotenv

folder_name = "images"

def get_file_extension(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    _, extension = os.path.splitext(filename)
    return extension


def downloading_images(url, filename):
    file_path = os.path.join(folder_name, filename)

    headers = {
        "User-Agent": "MyPythonScript/1.0 (https://example.com; myemail@example.com)"
    }

    # Проверка на наличие расширения
    _, extension = os.path.splitext(filename)
    if not extension:
        print(f"Ошибка: у файла {filename} отсутствует расширение. Пропуск загрузки.")
        return

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Сохранено: {file_path}")

    except requests.RequestException as e:
        print(f"Ошибка загрузки {url}: {e}")


def fetch_spacex_last_launch():
    spacex_url = "https://api.spacexdata.com/v5/launches/5eb87d42ffd86e000604b384"

    response = requests.get(spacex_url)
    response.raise_for_status()

    launch_data = response.json()

    photo_links = launch_data["links"].get("flickr", {}).get("original", [])

    for index, photo_url in enumerate(photo_links):
        filename = f"spacex_{index + 1}{get_file_extension(photo_url)}"
        downloading_images(photo_url, filename)


def download_nasa_images(api_key, count=20):
    nasa_url = "https://api.nasa.gov/planetary/apod"

    params = {"api_key": api_key, "count": count}

    try:
        response = requests.get(nasa_url, params=params)
        response.raise_for_status()

        images_data = response.json()

        for index, image in enumerate(images_data):
            url = image.get("url")
            filename = f"nasa_apod_{index + 1}{get_file_extension(url)}"
            downloading_images(url, filename)

    except requests.RequestException as e:
        print(f"Ошибка запроса к API NASA: {e}")


def fetch_epic_images(api_key, count=5):
    base_url = "https://epic.gsfc.nasa.gov/archive/natural"
    api_url = "https://api.nasa.gov/EPIC/api/natural/images"

    params = {"api_key": api_key}

    try:
        response = requests.get(api_url, params=params, timeout=10)
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
            filename = f"earth_{image_name}.png"

            downloading_images(image_url, filename)

    except requests.RequestException as e:
        print(f"Ошибка запроса к API NASA: {e}")


def main():
    load_dotenv()

    os.makedirs(folder_name, exist_ok=True)

    api_key = os.getenv("API_KEY")
    if not api_key or api_key == "YOUR_API_KEY":
        raise ValueError(
            "API_KEY не найден. Убедитесь, что он установлен в переменной окружения."
        )

    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    downloading_images(url, "hubble.jpeg")
    fetch_spacex_last_launch()
    download_nasa_images(api_key, count=20)
    fetch_epic_images(api_key, count=5)


if __name__ == "__main__":
    main()
