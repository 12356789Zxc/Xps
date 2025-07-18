import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an xpshort.com link and I'll bypass it for you!")

def bypass_link(url: str) -> str:
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})

        # 1st: Resolve xpshort.com
        r1 = session.get(url, allow_redirects=True, timeout=15)
        intermed_url = r1.url

        # 2nd: If redirected to qaluri or similar, resolve again
        if "qaluri.com" in intermed_url or "adlinkfly" in intermed_url:
            r2 = session.get(intermed_url, allow_redirects=True, timeout=15)
            return r2.url

        return intermed_url
    except Exception as e:
        logging.error(f"Error bypassing link: {e}")
        return "❌ Failed to bypass the link."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if "xpshort.com" in user_input:
        await update.message.reply_text("🔄 Bypassing...")
        result = bypass_link(user_input)
        await update.message.reply_text(f"✅ Final Link: {result}")
    else:
        await update.message.reply_text("❗ Please send a valid xpshort.com link.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
