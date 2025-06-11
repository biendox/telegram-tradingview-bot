import os
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, use_context=True)

# Command handlers
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Bot is running via webhook!")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="📩 Got your message!")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# TradingView webhook handler
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

# Set webhook when service starts
@app.before_first_request
def set_webhook():
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == "__main__":
    app.run(port=8080)
