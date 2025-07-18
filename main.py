import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any xpshort.com link and I'll bypass it for you!")

def bypass_xpshort(url: str) -> str:
    try:
        session = requests.Session()
        response = session.head(url, allow_redirects=True)
        return response.url
    except Exception as e:
        return f"Error: {str(e)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "xpshort.com" in text:
        final_url = bypass_xpshort(text.strip())
        await update.message.reply_text(f"Bypassed URL:\n{final_url}")
    else:
        await update.message.reply_text("Please send a valid xpshort.com link.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
