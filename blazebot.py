import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# Flask сервер
server = Flask(__name__)

# Токены
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
URL = os.getenv("RENDER_EXTERNAL_URL")  # Render сам подставляет URL

openai.api_key = OPENAI_API_KEY

# Создаем приложение Telegram
application = Application.builder().token(TELEGRAM_TOKEN).build()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, я Блейз!")

# чат
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = f"Я получил твое сообщение: {user_message}"
    await update.message.reply_text(reply)

# Подключаем хендлеры
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# Webhook для Telegram
@server.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Проверка Render
@server.route("/")
def home():
    return "Блейз бот работает!"

if __name__ == "__main__":
    # Устанавливаем webhook (один раз при старте)
    if URL:
        webhook_url = f"{URL}/{TELEGRAM_TOKEN}"
        application.bot.set_webhook(webhook_url)

    # Запуск Flask
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


