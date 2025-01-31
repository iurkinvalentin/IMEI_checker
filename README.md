# 📟 IMEI Checker API

## IMEI Checker API — это Django-приложение для проверки IMEI-номеров через внешний API. Оно включает REST API, Telegram-бота и механизм аутентификации.

## 🚀 Развертывание проекта локально

## 🔧 1. Клонирование репозитория
git clone https://github.com/iurkinvalentin/IMEI_checker.git
cd IMEI_checker
## 🏗 2. Создание виртуального окружения
python -m venv venv
Активация:

Windows:
venv\Scripts\activate
macOS/Linux:
source venv/bin/activate
## 📦 3. Установка зависимостей
pip install -r requirements.txt
## ⚙️ 4. Настройка переменных окружения
Создай файл .env в корне проекта и добавь:

SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
API_AUTH_TOKEN=your-api-auth-token
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
IMEI_API_URL=https://api.imeicheck.net/v1/checks
🔹 Обязательно замени your-secret-key и другие параметры на актуальные!

## 🛠 5. Применение миграций и запуск сервера
python manage.py migrate
python manage.py runserver
Теперь сервер работает на http://127.0.0.1:8000/ ✅

# 🎯 Тестирование API через Postman

##📌 1. Проверка IMEI
📍 POST http://127.0.0.1:8000/api/check-imei/

📩 Тело запроса (JSON):

{
  "imei": "123456789012345",
  "token": "your-api-auth-token"
}
📤 Ответ:

{
  "deviceName": "Apple iPhone 13",
  "simLock": false,
  "gsmaBlacklisted": false
}
##📌 2. Ошибочный IMEI
📍 POST http://127.0.0.1:8000/api/check-imei/

📩 Тело запроса (JSON):

{
  "imei": "invalid_imei",
  "token": "your-api-auth-token"
}
📤 Ответ:

{
  "error": "Invalid IMEI format"
}
##📌 3. Ошибочный токен
📍 POST http://127.0.0.1:8000/api/check-imei/

📩 Тело запроса (JSON):

{
  "imei": "123456789012345",
  "token": "wrong-token"
}
📤 Ответ:

{
  "error": "Unauthorized"
}
#🤖 Запуск Telegram-бота

python bot.py
Теперь бот слушает сообщения в Telegram! 📲

💬 Команды:

/start — Приветственное сообщение
Отправка IMEI-номера для проверки
🛠 Дополнительные команды

📍 Создание суперпользователя (для Django Admin):

python manage.py createsuperuser
📍 Просмотр логов сервера:

tail -f logs/server.log
📍 Остановка сервера:

CTRL + C
🏁 Готово!

Теперь твой проект развернут и протестирован через Postman. 🚀
📍 GitHub: https://github.com/iurkinvalentin/IMEI_checker

