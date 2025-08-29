# Multi-stage Dockerfile for KidSafe Alphabet Tutor
# Author: Nouran Darwish

FROM python:3.10-slim as builder

# Install system dependencies for audio, vision, and compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    libportaudio2 \
    tesseract-ocr \
    libtesseract-dev \
    ffmpeg \
    libsndfile1 \
    libgomp1 \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download models during build for faster runtime
# Download faster-whisper model
RUN python -c "from faster_whisper import WhisperModel; model = WhisperModel('small.en', device='cpu', compute_type='int8')"

# Download Silero VAD
RUN python -c "import torch; torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=False)"

# Download YOLOv8n model
RUN python -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt')"

# Production stage
FROM python:3.10-slim

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libportaudio2 \
    tesseract-ocr \
    ffmpeg \
    libsndfile1 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Create non-root user for security
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy pre-downloaded models
COPY --from=builder /root/.cache /home/appuser/.cache
RUN chown -R appuser:appuser /home/appuser/.cache

# Copy application code
COPY --chown=appuser:appuser . .

# Create necessary directories
RUN mkdir -p /app/models /app/logs /app/temp && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860 \
    OLLAMA_HOST=http://localhost:11434

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Expose Gradio port
EXPOSE 7860

# Start script to launch Ollama and the app
RUN echo '#!/bin/bash\n\
# Start Ollama in background\n\
ollama serve &\n\
sleep 5\n\
# Pull Llama model\n\
ollama pull llama3.2:3b\n\
# Start the application\n\
python app/gradio_ui.py' > /app/start.sh && \
    chmod +x /app/start.sh

# Run the application
CMD ["/app/start.sh"]