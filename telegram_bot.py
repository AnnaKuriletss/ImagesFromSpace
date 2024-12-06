import os
import time
import random
import argparse
from telegram import Bot
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)

chat_id = bot.get_updates()[-1].message.chat_id


def get_images_from_directory(directory):
    return [file for file in Path(directory).glob("*") if file.is_file()]

def publish_photos(directory, delay):
    images = get_images_from_directory(directory)

    while True:
        random.shuffle(images)
        for image in images:
            try:
                with open(image, "rb") as photo:
                    bot.send_photo(chat_id=chat_id, photo=photo, caption="Новое фото!")
                time.sleep(delay)
            except Exception as e:
                print(f"[{datetime.now()}] Ошибка отправки изображения {image}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт для публикации фото из директории в Telegram канал.")
    parser.add_argument(
        "--directory", 
        type=str, 
        default="images",
    )
    parser.add_argument(
        "--delay", 
        type=int, 
        default=int(os.getenv("PUBLISH_DELAY"))
    )
    args = parser.parse_args()

    publish_photos(args.directory, args.delay)
