# IndexTTS Dockerfile
FROM nvidia/cuda:12.8.0-cudnn9-runtime-ubuntu22.04

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

# Download IndexTTS-2 model (using HuggingFace mirror)
ENV HF_ENDPOINT="https://hf-mirror.com"
RUN uv tool install "huggingface-hub[cli,hf_xet]" && \
    ~/.local/bin/hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints

# Copy our API wrapper
COPY tts_api.py /app/tts_api.py

# Create output directory
RUN mkdir -p /app/output

# Set working directory back to /app
WORKDIR /app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command (using uv to run in the correct environment)
CMD ["python3", "tts_api.py"]

