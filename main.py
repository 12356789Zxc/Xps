import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an xpshort.com link to bypass.")

async def bypass_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "xpshort.com" not in url and "qaluri.com" not in url:
        await update.message.reply_text("Please send a valid xpshort.com or qaluri.com link.")
        return

    try:
        if "qaluri.com" in url:
            # Handle qaluri.com (AdLinkFly) links
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            # First request to get the page
            response = session.get(url, allow_redirects=True)
            
            # Look for the final URL in the page content
            content = response.text
            
            # Try to find the destination URL in various ways
            import re
            
            # Pattern 1: Look for go_url variable
            go_url_match = re.search(r'go_url\s*=\s*["\']([^"\']+)["\']', content)
            if go_url_match:
                final_url = go_url_match.group(1)
            else:
                # Pattern 2: Look for direct links in the content
                link_match = re.search(r'https?://(?!qaluri\.com)[^\s<>"\']+', content)
                if link_match:
                    final_url = link_match.group(0)
                else:
                    # If no direct link found, try to submit the form
                    form_match = re.search(r'<form[^>]*action="([^"]*)"[^>]*>', content)
                    if form_match:
                        form_action = form_match.group(1)
                        if form_action.startswith('/'):
                            form_action = 'https://qaluri.com' + form_action
                        
                        form_response = session.post(form_action, allow_redirects=True)
                        final_url = form_response.url
                    else:
                        final_url = response.url
        else:
            # Handle xpshort.com links (simple redirect)
            response = requests.get(url, allow_redirects=True)
            final_url = response.url
        
        await update.message.reply_text(f"Bypassed URL: {final_url}")
    except Exception as e:
        await update.message.reply_text("Error bypassing the link. Please try again later.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bypass_link))
    print("Bot started...")
    app.run_polling()
