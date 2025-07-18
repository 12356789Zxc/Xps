import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "YOUR_BOT_API_TOKEN"  # Replace this with your real token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a xpshort.com or qaluri.com link to bypass.")

def extract_final_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        if "xpshort.com" in url:
            session = requests.Session()
            resp = session.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            final_link = soup.find("a", attrs={"id": "go-link"})
            if final_link and final_link.has_attr("href"):
                return final_link["href"]
            # Fallback if id not found
            links = soup.find_all("a")
            for link in links:
                if link.get("href", "").startswith("http"):
                    return link["href"]

        elif "qaluri.com" in url:
            session = requests.Session()
            resp = session.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            final_link = soup.find("a", attrs={"id": "go-link"})
            if final_link and final_link.has_attr("href"):
                return final_link["href"]
            # Fallback
            links = soup.find_all("a")
            for link in links:
                if link.get("href", "").startswith("http"):
                    return link["href"]

    except Exception as e:
        print(f"Bypass error: {e}")
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "xpshort.com" in text or "qaluri.com" in text:
        await update.message.reply_text("Bypassing, please wait...")

        final_url = extract_final_url(text)
        if final_url:
            await update.message.reply_text(f"✅ Bypassed Link:\n{final_url}")
        else:
            await update.message.reply_text("❌ Failed to bypass the link. Try another one.")
    else:
        await update.message.reply_text("Please send a xpshort.com or qaluri.com link.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
