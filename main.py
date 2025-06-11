import os
import telegram

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"

bot = telegram.Bot(token=TOKEN)

# Force reset: delete polling & set webhook clean
bot.delete_webhook()
bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

print("✅ Webhook reset successfully!")
