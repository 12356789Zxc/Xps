import telebot
import requests
from bs4 import BeautifulSoup
import re
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set this in Railway as environment variable
bot = telebot.TeleBot(BOT_TOKEN)

def bypass_adlinkfly(url):
    if "xpshort.com" in url:
        domain = "xpshort.com"
    elif "qaluri.com" in url:
        domain = "qaluri.com"
    else:
        return "❗ Please send a valid xpshort.com or qaluri.com link."

    try:
        session = requests.Session()
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        token_tag = soup.find("input", {"name": "_token"})

        if not token_tag:
            return "❗ Unable to find token on the page."

        token = token_tag.get("value")
        headers = {"X-Requested-With": "XMLHttpRequest"}
        payload = {"_token": token}
        go_link = f"https://{domain}/links/go"
        final_response = session.post(go_link, headers=headers, data=payload)

        if final_response.status_code == 200 and "url" in final_response.json():
            return f"✅ Bypassed Link:\n{final_response.json()['url']}"
        else:
            return "❗ Failed to bypass the link. Try again."
    except Exception as e:
        return f"❗ Error occurred: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    if "xpshort.com" in url or "qaluri.com" in url:
        bot.reply_to(message, "⏳ Bypassing the link, please wait...")
        result = bypass_adlinkfly(url)
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "❗ Please send a valid xpshort.com or qaluri.com link.")

print("✅ Bot is running...")
bot.polling()
