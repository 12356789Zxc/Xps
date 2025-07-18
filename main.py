import os
import re
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Telegram Bot Token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN not set in environment variables!")
    exit("❌ BOT_TOKEN not set. Set it in Railway or your .env file.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot.")
    await message.reply("👋 Send me an xpshort.com link and I’ll try to bypass it!")

@dp.message_handler()
async def handle_message(message: types.Message):
    url = message.text.strip()

    if not re.match(r"https?://xpshort\.com/\S+", url):
        logger.warning(f"User {message.from_user.id} sent invalid link: {url}")
        await message.reply("❌ Please send a valid xpshort.com link.")
        return

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)

        if response.ok:
            bypassed_url = response.url
            logger.info(f"Bypassed URL for user {message.from_user.id}: {bypassed_url}")
            await message.reply(f"✅ Bypassed Link:\n\n{url} → {bypassed_url}")
        else:
            logger.error(f"Failed request for {url} - status code: {response.status_code}")
            await message.reply("❌ Couldn't bypass this link. Please try another.")

    except Exception as e:
        logger.exception("Error during bypass")
        await message.reply(f"❌ Error while bypassing:\n{str(e)}")

if __name__ == "__main__":
    logger.info("🚀 Bot is starting up...")
    executor.start_polling(dp, skip_updates=True)
