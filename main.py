import os
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

# Get environment variables
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"

# Initialize bot and app
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, use_context=True)

# Telegram command handlers
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Bot is running via webhook!")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋 I'm here!")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# TradingView alert endpoint
@app.route("/alert", methods=["POST"])
def alert():
    data = request.json
    message = f"📢 *Signal Alert*\n{data.get('ticker')}\nDirection: *{data.get('direction')}*\nPrice: {data.get('price')}\n\nReason:\n{data.get('description')}"
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
    return "ok"

# Telegram webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Set the webhook and run the server
if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=8080)
