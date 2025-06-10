from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Load Telegram bot credentials from environment variables
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_USER_ID = os.environ.get('TELEGRAM_USER_ID')  # Your personal handle/user ID

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_USER_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if not data:
        return "No data received", 400

    # Customize how the message looks based on TradingView alert content
    symbol = data.get("symbol", "Unknown")
    direction = data.get("direction", "No direction")
    entry = data.get("entry", "N/A")
    sl = data.get("sl", "N/A")
    tp = data.get("tp", "N/A")
    logic = data.get("logic", "No description")

    message = f"""
📡 *Signal Alert*
*{symbol}*  
*Direction:* {direction.upper()}
*Entry:* {entry}
*SL:* {sl}
*TP:* {tp}

📖 *Setup Logic:*  
{logic}
    """

    send_telegram_message(message.strip())
    return "Signal Sent", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
