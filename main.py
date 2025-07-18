import logging
import re
import requests
import os
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv("BOT_TOKEN")  # Reads the token from Railway environment

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Regex pattern to detect xpshort links
XPSHORT_PATTERN = re.compile(r'(https?://xpshort\.com/\S+)')

def bypass_xpshort(url):
    try:
        session = requests.Session()
        response = session.head(url, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        return f"❌ Error: {e}"

@dp.message_handler()
async def handle_message(message: types.Message):
    links = XPSHORT_PATTERN.findall(message.text)
    if not links:
        return  # No xpshort link in message

    results = []
    for link in links:
        final_url = bypass_xpshort(link)
        results.append(f"🔗 Original: {link}\n➡️ Final: {final_url}")

    await message.reply("\n\n".join(results))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
