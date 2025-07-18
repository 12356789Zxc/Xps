FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Browsers
RUN apt-get update && apt-get install -y wget curl unzip fonts-liberation libnss3 libatk1.0-0 libatk-bridge2.0-0 libxss1 libasound2 libx11-xcb1 libgbm1 libgtk-3-0 libdrm2 libxcomposite1 libxdamage1 libxrandr2
RUN python -m playwright install chromium

CMD ["python", "bot.py"]
