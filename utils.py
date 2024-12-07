import os
from urllib.parse import urlparse
import requests


def get_file_extension(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    _, extension = os.path.splitext(filename)
    return extension


def downloading_images(url, folder_name, filename):
    folder_name = "images"
    os.makedirs(folder_name, exist_ok=True)
    file_path = os.path.join(folder_name, filename)

    if not get_file_extension(url):
        print(f"Ошибка: у файла {filename} отсутствует расширение. Пропуск загрузки.")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(file_path, "wb") as file:
            file.write(response.content)
    except requests.RequestException as e:
        print(f"Ошибка загрузки {url}: {e}")
