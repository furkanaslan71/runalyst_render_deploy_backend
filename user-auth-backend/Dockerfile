# Dockerfile for Production on Render

FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# 1. OPTIMIZATION: Clean up apt-get to reduce image size
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
# (Make sure to use a .dockerignore file - see below)
COPY . .

# EXPOSE is not strictly required by Render but is good practice
EXPOSE 8000

# 2. CRITICAL CHANGE: Use Gunicorn for production
# This command starts a production-ready server that listens on the port
# provided by Render's $PORT environment variable.
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:${PORT}"]