from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")

if not token:
    raise ValueError("Токен бота не найден. Проверьте файл .env.")

bot = Bot(token=token)

chat_id = bot.get_updates()[-1].message.chat_id

try:
    bot.send_message(chat_id=chat_id, text="Привет! Добро пожаловать в мой канал!")
    print("Сообщение отправлено в канал.")
except Exception as e:
    print(f"Ошибка отправки сообщения: {e}")
