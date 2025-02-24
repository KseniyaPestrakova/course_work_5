import requests

from config.settings import BOT_TOKEN, TELEGRAM_URL


def send_telegram_message(message, chat_id):
    """Отправка сообщения в Telegram."""
    params = {"text": message, "chat_id": chat_id}

    requests.get(f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", params=params)
