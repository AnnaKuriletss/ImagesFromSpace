import os
from telegram import Bot, ChatAction
from telegram.error import TelegramError
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")

if not token:
    raise ValueError("Токен бота не найден. Проверьте файл .env.")

bot = Bot(token=token)

chat_id = bot.get_updates()[-1].message.chat_id 


image_path = "images/spacex_1.jpg"  

def send_action(action):
    def decorator(func):
        def command_function(*args, **kwargs):
            bot.send_chat_action(chat_id=chat_id, action=action)
            return func(*args, **kwargs)
        return command_function
    return decorator

send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)

@send_upload_photo_action
def send_photo_with_action():
    with open(image_path, "rb") as image_file:
        bot.send_photo(chat_id=chat_id, photo=image_file)

try:
    send_photo_with_action()
except TelegramError as e:
    print(f"Ошибка отправки: {e}")
except FileNotFoundError:
    print("Файл с изображением не найден. Проверьте путь.")
