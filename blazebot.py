import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# ------------------------------
# Flask для Render
# ------------------------------
server = Flask(__name__)

# ------------------------------
# Ключи из переменных окружения
# ------------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# ------------------------------
# Создаём Application Telegram
# ------------------------------
application = Application.builder().token(TELEGRAM_TOKEN).build()

# ------------------------------
# Обработчики команд и сообщений
# ------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет. Я Блейз. Строгий и рассудительный собеседник."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты строгий и рассудительный персонаж по имени Блейз."},
                {"role": "user", "content": user_message},
            ],
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Ошибка: {e}"

    await update.message.reply_text(reply)

# Регистрируем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

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
    return "Блейз бот работает!"

# ------------------------------
# Запуск Flask
# ------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
