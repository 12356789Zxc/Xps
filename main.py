
import logging
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token here
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Define a function to handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.strip()

    # Regex patterns
    xpshort_pattern = r'https?://(?:www\.)?xpshort\.com/(\w+)'
    qaluri_pattern = r'https?://(?:www\.)?qaluri\.com/\?adlinkfly=(\w+)'

    # Check if the message matches xpshort
    xpshort_match = re.search(xpshort_pattern, message_text)
    qaluri_match = re.search(qaluri_pattern, message_text)

    if xpshort_match:
        code = xpshort_match.group(1)
        await update.message.reply_text("🔄 Bypassing xpshort...")
        try:
            # Simulated bypass logic for xpshort (replace with actual if needed)
            final_url = f"https://qaluri.com/?adlinkfly={code}"
            await update.message.reply_text(f"✅ Final Link: {final_url}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        return

    elif qaluri_match:
        code = qaluri_match.group(1)
        await update.message.reply_text("🔄 Bypassing qaluri...")
        try:
            # Simulated bypass logic for qaluri (replace with actual if needed)
            final_url = f"https://finaldestination.com/redirect/{code}"  # Replace with your logic
            await update.message.reply_text(f"✅ Final Link: {final_url}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        return

    else:
        await update.message.reply_text("❗ Please send a valid xpshort.com or qaluri.com link.")

# Define a function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("👋 Send me a xpshort.com or qaluri.com link to bypass.")

# Main function to start the bot
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
