import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to bypass xpshort links
def bypass_xpshort(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        return f"❌ Error: {e}"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! Send me any xpshort.com link and I’ll bypass it for you.")

# Handler for normal messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "xpshort.com/" in text:
        await update.message.reply_text("⏳ Bypassing your link... Please wait.")
        result = bypass_xpshort(text)
        await update.message.reply_text(f"✅ Final URL:\n{result}")
    else:
        await update.message.reply_text("⚠️ Please send only valid xpshort.com links.")

# Main bot function
def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("❌ BOT_TOKEN not set. Make sure it's added as an environment variable.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run bot
    print("✅ Bot is running...")
    app.run_polling()

# Entry point
if __name__ == '__main__':
    main()
