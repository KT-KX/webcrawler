# Use a Python base image
FROM python:3.11-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    libgtk-3-0 \
    libx11-xcb1 \
    libdbus-glib-1-2 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libxss1 \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxrandr2 \
    libgbm1 \
    --no-install-recommends

# Install Python dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright and its dependencies
RUN pip install playwright
RUN playwright install chromium --with-deps

# Copy your application code into the container
COPY . /app/

# Expose the app port
EXPOSE 8080

# Set the entrypoint for your Flask app
CMD ["python", "app.py"]
