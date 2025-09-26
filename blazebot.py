import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ------------------------------
# Flask для Render
# ------------------------------
server = Flask(__name__)

# ------------------------------
# Ключи из переменных окружения
# ------------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# ------------------------------
# Создаём Application Telegram
# ------------------------------
application = Application.builder().token(TELEGRAM_TOKEN).build()

# ------------------------------
# Обработчики команд и сообщений
# ------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Блейз (эхо-версия). Пиши что угодно, и я повторю."
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"Эхо: {user_message}")

# Регистрируем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ------------------------------
# Webhook для Telegram
# ------------------------------
@server.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return "ok"

# Простая домашняя страница
@server.route("/")
def home():
    return "Блейз бот (эхо) работает!"

# ------------------------------
# Запуск Flask
# ------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
