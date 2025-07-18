import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# ✅ Load your BOT TOKEN securely from Railway variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🟢 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send any xpshort.com link to bypass.")

# 🟢 Handles xpshort.com links
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "xpshort.com/" in url:
        try:
            response = requests.get(url, allow_redirects=True, timeout=10)
            final_url = response.url
            await update.message.reply_text(f"🔗 Final link: {final_url}")
        except Exception as e:
            await update.message.reply_text("❌ Failed to bypass the link.")
    else:
        await update.message.reply_text("⚠️ Please send a valid xpshort.com link.")

# 🟢 Start the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()
