# IndexTTS Dockerfile
# This image contains IndexTTS code and dependencies, but NOT the model files
# Model files should be mounted as a volume at runtime
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    git-lfs \
    wget \
    curl \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Enable Git LFS
RUN git lfs install

# Clone IndexTTS repository
RUN git clone https://github.com/index-tts/index-tts.git /app/index-tts && \
    cd /app/index-tts && \
    git lfs pull

# Install uv package manager
RUN pip3 install --no-cache-dir uv

# Install IndexTTS dependencies
WORKDIR /app/index-tts
RUN uv sync --all-extras --default-index "https://mirrors.aliyun.com/pypi/simple"

# Copy our API wrapper
COPY tts_api.py /app/tts_api.py

# Create necessary directories
RUN mkdir -p /app/checkpoints /app/output /app/examples

# Set working directory back to /app
WORKDIR /app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Environment variables (can be overridden at runtime)
ENV MODEL_PATH=/app/checkpoints
ENV OUTPUT_PATH=/app/output
ENV USE_FP16=true
ENV MAX_WORKERS=4

# Start command
CMD ["python3", "tts_api.py"]

