import os
import re
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Load Telegram Bot Token from Environment Variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("👋 Send an xpshort.com link, and I'll try to bypass it.")

@dp.message_handler()
async def handle_message(message: types.Message):
    url = message.text.strip()

    if not re.match(r"https?://xpshort\.com/\S+", url):
        await message.reply("❌ Please send a valid xpshort.com link.")
        return

    # === Fake Bypass Logic ===
    # Replace this later with real bypass code
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        # Placeholder: simulate a real link for now
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        bypassed_url = response.url if response.ok else "https://example.com"
        await message.reply(f"✅ Bypassed Link:\n\n{url} → {bypassed_url}")
    except Exception as e:
        await message.reply(f"❌ Failed to bypass link.\nError: {str(e)}")

if __name__ == "__main__":
    executor.start_polling(dp)
