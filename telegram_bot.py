import os
import time
import random
import argparse
from telegram import Bot, TelegramError
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime


def get_images_from_directory(directory):
    return [file for file in Path(directory).glob("*") if file.is_file()]


def publish_photos(directory, delay, send_photo_action):
    images = get_images_from_directory(directory)

    while True:
        random.shuffle(images)
        for image in images:
            try:
                with open(image, "rb") as photo:
                    send_photo_action(photo)
                time.sleep(delay)
            except TelegramError as e:
                print(
                    f"[{datetime.now()}] Ошибка при запросе обновлений у Telegram: {e}"
                )


def main():

    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")

    bot = Bot(token=token)

    chat_id = bot.get_updates()[-1].message.chat_id
    parser = argparse.ArgumentParser(
        description="Скрипт для публикации фото из директории в Telegram канал."
    )
    parser.add_argument(
        "--directory",
        type=str,
        default="images",
    )
    parser.add_argument("--delay", type=int, default=int(os.getenv("PUBLISH_DELAY")))
    args = parser.parse_args()

    send_photo_action = lambda photo: bot.send_photo(
        chat_id=chat_id, photo=photo, caption="Новое фото!"
    )

    publish_photos(args.directory, args.delay, send_photo_action)


if __name__ == "__main__":
    main()
