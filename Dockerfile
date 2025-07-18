# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY . .

# Set environment variable for Python
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "main.py"]
