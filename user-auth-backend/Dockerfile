FROM python:3.11-slim
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# CRITICAL: Before the CMD, ensure the script is executable
RUN chmod +x ./render-start.sh

# This is the NEW CMD. It tells the container to run our script on startup.
CMD ["./render-start.sh"]
