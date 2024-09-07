# Backend Dockerfile (Flask + Whisper + FFmpeg)

FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Set working directory
WORKDIR /app

# Install system dependencies (FFmpeg)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (including Whisper from PyPI)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ ./

# Expose the Flask port (9010)
EXPOSE 9010

# Run the Flask app
CMD ["python", "app.py"]
