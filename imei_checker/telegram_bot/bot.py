import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imei_checker.settings")
django.setup()

import requests
import logging
from django.conf import settings
from telegram import Update
from telegram.ext import (Application, CommandHandler,
                          MessageHandler, filters, CallbackContext)
from api.models import AllowedUser
from asgiref.sync import sync_to_async

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TELEGRAM_TOKEN = settings.TELEGRAM_BOT_TOKEN


def check_imei_api(imei):
    """Проверяет IMEI через API."""
    url = settings.IMEI_API_URL
    headers = {
        "Authorization": f"Bearer {settings.API_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"deviceId": imei, "serviceId": 12}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"IMEI check request failed: {e}")
        return {"error": "Service unavailable"}


@sync_to_async
def is_user_allowed(user_id):
    """Проверяет доступ пользователя."""
    return AllowedUser.objects.filter(user_id=user_id).exists()


async def start(update: Update, context: CallbackContext):
    """Отправляет приветствие"""
    user_id = update.effective_user.id
    if not await is_user_allowed(user_id):
        await update.message.reply_text("🚫 Доступ запрещен.")
        return
    await update.message.reply_text("👋 Привет! Отправь IMEI для проверки.")


async def handle_message(update: Update, context: CallbackContext):
    """Обрабатывает текстовые сообщения"""
    user_id = update.effective_user.id
    if not await is_user_allowed(user_id):
        await update.message.reply_text("🚫 Доступ запрещен.")
        return

    imei = update.message.text.strip()
    if not imei.isdigit() or len(imei) not in [15, 17]:
        await update.message.reply_text("⚠️ Некорректный формат IMEI.")
        return

    await update.message.reply_text("🔍 Проверяю IMEI, подождите...")

    data = check_imei_api(imei)
    if "error" in data:
        await update.message.reply_text("❌ Ошибка при проверке IMEI.")
        return

    response_text = f"📱 IMEI: {imei}\n"
    if "properties" in data:
        props = data["properties"]

        response_text += (
            f"📌 Устройство: {props.get('deviceName', 'Неизвестно')}\n"
            f"🔒 SIM-лок: {'Да' if props.get('simLock', False) else 'Нет'}\n"
            f"🚨 В черном списке: "
            f"{'Да' if props.get('gsmaBlacklisted', False) else 'Нет'}\n"
        )

    await update.message.reply_text(response_text)


def run_bot():
    """Запуск"""
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("🤖 Бот запущен. Ожидаю сообщения...")

    app.run_polling()


if __name__ == "__main__":
    run_bot()
