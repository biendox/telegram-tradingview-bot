import os
from flask import Flask, request
from telegram import Bot, Update, ParseMode
from telegram.ext import CommandHandler, Dispatcher, MessageHandler, Filters
import threading

app = Flask(__name__)

# Environment variables
TELEGRAM_TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# Set up dispatcher for message handling
from telegram.ext import Dispatcher

dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# Handle /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Bot is running and ready!")

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

# Optional: handle random text messages
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋 I'm here!")

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Flask route to receive TradingView alerts
@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    message = f"📢 *Signal Alert*\n{data.get('ticker')}\nDirection: *{data.get('direction')}*\nPrice: {data.get('price')}\n\nReason:\n{data.get('description')}"
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.MARKDOWN)
    return 'ok'

# Poll Telegram messages in a background thread
def run_dispatcher():
    from telegram.ext import Updater
    updater = Updater(bot=bot, use_context=True)
    updater.start_polling()

threading.Thread(target=run_dispatcher).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
