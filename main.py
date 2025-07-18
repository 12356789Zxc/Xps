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
            await update.message.reply_text("🔄 Processing qaluri.com link... This will take about 1-2 minutes.")
            
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': url
            })
            
            current_url = url
            
            # Step 1: "I'm not a robot" button + 28 seconds timer
            await update.message.reply_text("🤖 Step 1/3: Clicking 'I'm not a robot' button...")
            
            response = session.get(current_url, allow_redirects=True)
            current_url = response.url  # Handle any redirects
            content = response.text
            
            # Look for "I'm not a robot" button
            robot_button = re.search(r'<button[^>]*(?:robot|verify|captcha)[^>]*onclick="([^"]*)"[^>]*>', content, re.IGNORECASE)
            if not robot_button:
                robot_button = re.search(r'<button[^>]*onclick="([^"]*)"[^>]*>.*?(?:robot|verify|captcha).*?</button>', content, re.IGNORECASE)
            
            if robot_button:
                onclick_action = robot_button.group(1)
                # Extract URL from onclick if present
                onclick_url = re.search(r'(?:location\.href|window\.location)\s*=\s*["\']([^"\']+)["\']', onclick_action)
                if onclick_url:
                    current_url = onclick_url.group(1)
                    if current_url.startswith('/'):
                        current_url = 'https://qaluri.com' + current_url
            
            # Wait 28 seconds
            await update.message.reply_text("⏳ Waiting 28 seconds...")
            time.sleep(28)
            
            # Step 2: "CLICK 2X FOR GENERATE LINK" button
            await update.message.reply_text("🔗 Step 2/3: Looking for 'CLICK 2X FOR GENERATE LINK' button...")
            
            response = session.get(current_url, allow_redirects=True)
            current_url = response.url  # Handle any redirects
            content = response.text
            
            # Look for "CLICK 2X FOR GENERATE LINK" button
            generate_button = re.search(r'<button[^>]*(?:generate|click.*2x|2x.*click)[^>]*onclick="([^"]*)"[^>]*>', content, re.IGNORECASE)
            if not generate_button:
                generate_button = re.search(r'<button[^>]*onclick="([^"]*)"[^>]*>.*?(?:generate|click.*2x|2x.*click).*?</button>', content, re.IGNORECASE)
            
            if generate_button:
                onclick_action = generate_button.group(1)
                onclick_url = re.search(r'(?:location\.href|window\.location)\s*=\s*["\']([^"\']+)["\']', onclick_action)
                if onclick_url:
                    current_url = onclick_url.group(1)
                    if current_url.startswith('/'):
                        current_url = 'https://qaluri.com' + current_url
            
            # Wait 5 seconds
            await update.message.reply_text("⏳ Waiting 5 seconds...")
            time.sleep(5)
            
            # Step 3: "download link" button
            await update.message.reply_text("📥 Step 3/3: Looking for 'download link' button...")
            
            response = session.get(current_url, allow_redirects=True)
            current_url = response.url  # Handle any redirects
            content = response.text
            
            # Look for "download link" button - this should contain the final URL
            download_button = re.search(r'<button[^>]*(?:download|final)[^>]*onclick="([^"]*)"[^>]*>', content, re.IGNORECASE)
            if not download_button:
                download_button = re.search(r'<button[^>]*onclick="([^"]*)"[^>]*>.*?(?:download|final).*?</button>', content, re.IGNORECASE)
            
            final_url = None
            
            if download_button:
                onclick_action = download_button.group(1)
                onclick_url = re.search(r'(?:location\.href|window\.location)\s*=\s*["\']([^"\']+)["\']', onclick_action)
                if onclick_url:
                    final_url = onclick_url.group(1)
                    if final_url.startswith('/'):
                        final_url = 'https://qaluri.com' + final_url
            
            # Alternative: Look for direct href in download button
            if not final_url:
                download_href = re.search(r'<a[^>]*href="([^"]*)"[^>]*>.*?(?:download|final).*?</a>', content, re.IGNORECASE)
                if download_href:
                    final_url = download_href.group(1)
            
            # Alternative: Look for external URLs (not qaluri.com)
            if not final_url:
                external_urls = re.findall(r'https?://(?!qaluri\.com)[^\s<>"\']+', content)
                for ext_url in external_urls:
                    if not any(ad_domain in ext_url.lower() for ad_domain in ['ads', 'ad.', 'doubleclick', 'google', 'facebook', 'adsystem']):
                        final_url = ext_url
                        break
            
            if final_url and final_url != current_url:
                await update.message.reply_text(f"✅ Final destination URL: {final_url}")
            else:
                await update.message.reply_text(f"⚠️ Could not find final destination. Last URL: {current_url}")
                
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
