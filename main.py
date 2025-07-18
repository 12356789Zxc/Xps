import logging
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

API_TOKEN = "YOUR_BOT_API_TOKEN"  # Replace this with your bot's token

# Function to bypass xpshort.com
def bypass_xpshort(url):
    try:
        session = requests.Session()
        resp = session.get(url, timeout=10)
        if "Location" in resp.history[-1].headers:
            return resp.history[-1].headers["Location"]
        return resp.url
    except Exception as e:
        logging.error(f"xpshort bypass error: {e}")
        return None

# Function to bypass qaluri.com
def bypass_qaluri(url):
    try:
        session = requests.Session()
        resp = session.get(url, timeout=10, allow_redirects=True)
        return resp.url
    except Exception as e:
        logging.error(f"qaluri bypass error: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a xpshort.com or qaluri.com link to bypass.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    xpshort_pattern = r"(https?://)?(www\.)?xpshort\.com/\S+"
    qaluri_pattern = r"(https?://)?(www\.)?qaluri\.com/\S+"

    if re.match(xpshort_pattern, text):
        await update.message.reply_text("🔄 Bypassing xpshort...")
        result = bypass_xpshort(text)
        if result:
            await update.message.reply_text(f"✅ Final Link: {result}")
        else:
            await update.message.reply_text("❌ Failed to bypass xpshort link.")
    elif re.match(qaluri_pattern, text):
        await update.message.reply_text("🔄 Bypassing qaluri...")
        result = bypass_qaluri(text)
        if result:
            await update.message.reply_text(f"✅ Final Link: {result}")
        else:
            await update.message.reply_text("❌ Failed to bypass qaluri link.")
    else:
        await update.message.reply_text("❗ Please send a valid xpshort.com or qaluri.com link.")

def main():
    app = ApplicationBuilder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()