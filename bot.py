from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from playwright.sync_api import sync_playwright
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

def bypass_xpshort(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            page.wait_for_timeout(10000)  # wait for redirect
            final_url = page.url
            browser.close()
            return final_url
    except Exception as e:
        return f"❌ Error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send any xpshort.com link to bypass.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.startswith("https://xpshort.com/"):
        await update.message.reply_text("⏳ Bypassing...")
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, bypass_xpshort, text)
        await update.message.reply_text(f"🔗 Final link:\n{result}")
    else:
        await update.message.reply_text("⚠️ Please send a valid xpshort.com link.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
