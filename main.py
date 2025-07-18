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
            import re
            import time
            
            # Send initial message
            await update.message.reply_text("🔄 Processing qaluri.com link... This may take up to 2 minutes.")
            
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            })
            
            current_url = url
            
            # Go through the multi-step process
            for step in range(1, 4):  # 3 steps
                await update.message.reply_text(f"⏳ Step {step}/3 - Waiting 25 seconds...")
                
                response = session.get(current_url, allow_redirects=True)
                content = response.text
                
                # Wait 25 seconds (simulating the timer)
                time.sleep(25)
                
                # Look for the continue/next step URL
                continue_match = re.search(r'href="([^"]*(?:continue|next|step)[^"]*)"', content, re.IGNORECASE)
                if not continue_match:
                    # Alternative patterns
                    continue_match = re.search(r'url\s*:\s*["\']([^"\']+)["\']', content)
                    if not continue_match:
                        continue_match = re.search(r'window\.location\.href\s*=\s*["\']([^"\']+)["\']', content)
                
                if continue_match:
                    next_url = continue_match.group(1)
                    if next_url.startswith('/'):
                        next_url = 'https://qaluri.com' + next_url
                    elif not next_url.startswith('http'):
                        next_url = 'https://qaluri.com/' + next_url
                    
                    current_url = next_url
                else:
                    # Try to find form submission
                    form_match = re.search(r'<form[^>]*action="([^"]*)"[^>]*>', content)
                    if form_match:
                        form_action = form_match.group(1)
                        if form_action.startswith('/'):
                            form_action = 'https://qaluri.com' + form_action
                        
                        # Submit the form
                        form_data = {}
                        input_matches = re.findall(r'<input[^>]*name="([^"]*)"[^>]*value="([^"]*)"[^>]*>', content)
                        for name, value in input_matches:
                            form_data[name] = value
                        
                        response = session.post(form_action, data=form_data, allow_redirects=True)
                        current_url = response.url
            
            # Final step - get the destination URL
            final_response = session.get(current_url, allow_redirects=True)
            final_content = final_response.text
            
            # Look for the final destination URL
            dest_match = re.search(r'go_url\s*=\s*["\']([^"\']+)["\']', final_content)
            if not dest_match:
                dest_match = re.search(r'https?://(?!qaluri\.com)[^\s<>"\']+', final_content)
            
            if dest_match:
                final_url = dest_match.group(1) if hasattr(dest_match, 'group') else dest_match.group(0)
                await update.message.reply_text(f"✅ Bypassed URL: {final_url}")
            else:
                await update.message.reply_text(f"⚠️ Could not extract final URL. Last URL: {current_url}")
                
        else:
            # Handle xpshort.com links (simple redirect)
            response = requests.get(url, allow_redirects=True)
            final_url = response.url
            await update.message.reply_text(f"✅ Bypassed URL: {final_url}")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error bypassing the link: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bypass_link))
    print("Bot started...")
    app.run_polling()
