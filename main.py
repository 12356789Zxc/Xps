import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an xpshort.com link to bypass.")

async def bypass_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "xpshort.com" not in url:
        await update.message.reply_text("Please send a valid xpshort.com link.")
        return

    try:
        response = requests.get(url, allow_redirects=True)
        final_url = response.url
        await update.message.reply_text(f"Bypassed URL: {final_url}")
    except Exception as e:
        await update.message.reply_text("Error bypassing the link. Please try again later.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bypass_link))
    print("Bot started...")
    app.run_polling()