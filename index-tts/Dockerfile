# IndexTTS Dockerfile
# This image contains IndexTTS code and dependencies, but NOT the model files
# Model files should be mounted as a volume at runtime
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Set working directory
WORKDIR /app

# Set environment to reduce disk usage
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1
ENV UV_NO_CACHE=1

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
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Enable Git LFS
RUN git lfs install

# Clone IndexTTS repository (shallow clone to save space)
RUN git clone --depth 1 https://github.com/index-tts/index-tts.git /app/index-tts

# Install uv package manager
RUN pip3 install --no-cache-dir uv

# Install IndexTTS dependencies
WORKDIR /app/index-tts

# Install PyTorch with CUDA 11.8 (compatible with our base image)
# Using older PyTorch version to reduce size
RUN pip3 install --no-cache-dir \
    torch==2.1.2 \
    torchaudio==2.1.2 \
    --index-url https://download.pytorch.org/whl/cu118 \
    && rm -rf /root/.cache/pip

# Install core dependencies one by one to manage disk space
RUN pip3 install --no-cache-dir \
    accelerate==1.8.1 \
    cn2an==0.5.22 \
    einops==0.8.1 \
    && rm -rf /root/.cache/pip

RUN pip3 install --no-cache-dir \
    librosa==0.10.2 \
    numpy==1.26.2 \
    omegaconf==2.3.0 \
    && rm -rf /root/.cache/pip

RUN pip3 install --no-cache-dir \
    transformers==4.52.1 \
    tokenizers==0.21.0 \
    sentencepiece==0.2.1 \
    && rm -rf /root/.cache/pip

RUN pip3 install --no-cache-dir \
    jieba==0.42.1 \
    g2p-en==2.1.0 \
    ffmpeg-python==0.2.0 \
    && rm -rf /root/.cache/pip

RUN pip3 install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn==0.32.0 \
    pydantic==2.10.0 \
    && rm -rf /root/.cache/pip

# Install remaining dependencies
RUN pip3 install --no-cache-dir \
    safetensors==0.5.2 \
    tqdm==4.67.1 \
    munch==4.0.0 \
    && rm -rf /root/.cache/pip

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

