import os
import re
import requests
from urllib.parse import urlparse
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

# Function to bypass xpshort and qaluri
def bypass_adlinkfly(url: str) -> str:
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    try:
        res = session.get(url, headers=headers)
        final_url = res.url

        if "go?" in final_url or "locked" in final_url:
            parts = final_url.split("?")
            main = parts[0].replace("go", "links/go")
            token = parts[1]
            api_url = f"{main}?{token}"
            response = session.get(api_url, headers=headers)
            if response.status_code == 200 and "url" in response.text:
                return response.text.split("url\":\"")[1].split("\"")[0].replace("\\", "")
    except Exception as e:
        print("Bypass error:", e)

    return None

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔗 Send me a link from xpshort.com or qaluri.com to bypass it!")

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if any(domain in url for domain in ["xpshort.com", "qaluri.com"]):
        await update.message.reply_text("⏳ Bypassing link... please wait.")
        final_link = bypass_adlinkfly(url)

        if final_link:
            await update.message.reply_text(f"✅ Final Link:\n{final_link}")
        else:
            await update.message.reply_text("❌ Failed to bypass the link. Please check and try again.")
    else:
        await update.message.reply_text("❗ Please send a valid xpshort.com or qaluri.com link.")

# Run the bot
if __name__ == "__main__":
    if not TOKEN:
        print("❌ BOT_TOKEN is not set. Please set it in Railway's environment variables.")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.run_polling()
