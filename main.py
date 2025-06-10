import os
from flask import Flask, request
import telegram

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
bot = telegram.Bot(token=TELEGRAM_TOKEN)

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    message = f"📢 *Signal Alert*\n{data.get('ticker')}\nDirection: *{data.get('direction')}*\nPrice: {data.get('price')}\n\nReason:\n{data.get('description')}"
    bot.send_message(chat_id=TELEGRAM_USER_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
    return 'ok'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)