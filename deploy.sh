#!/bin/bash

# AI Services Deployment Script
# Usage: ./deploy.sh [build|push|deploy|all]

set -e

DOCKER_USERNAME="p971607"
INDEX_TTS_IMAGE="${DOCKER_USERNAME}/index-tts:latest"
COMFYUI_IMAGE="${DOCKER_USERNAME}/comfyui:latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Build images
build_images() {
    echo_info "Building Docker images..."
    
    echo_info "Building IndexTTS image..."
    docker build -t ${INDEX_TTS_IMAGE} ./index-tts
    
    echo_info "Building ComfyUI image..."
    docker build -t ${COMFYUI_IMAGE} ./comfyui
    
    echo_info "Build completed successfully!"
}

# Push images to Docker Hub
push_images() {
    echo_info "Pushing images to Docker Hub..."
    
    # Check if logged in
    if ! docker info | grep -q "Username: ${DOCKER_USERNAME}"; then
        echo_warn "Not logged in to Docker Hub. Logging in..."
        docker login
    fi
    
    echo_info "Pushing IndexTTS image..."
    docker push ${INDEX_TTS_IMAGE}
    
    echo_info "Pushing ComfyUI image..."
    docker push ${COMFYUI_IMAGE}
    
    echo_info "Push completed successfully!"
}

# Deploy with Docker Compose
deploy_local() {
    echo_info "Deploying services locally with Docker Compose..."
    
    # Create data directories
    mkdir -p data/{checkpoints,output,examples,models,comfyui-output,comfyui-input}
    
    # Start services
    docker-compose up -d
    
    echo_info "Services deployed successfully!"
    echo_info "IndexTTS: http://localhost:8000"
    echo_info "ComfyUI: http://localhost:8001"
    
    # Show logs
    echo_info "Showing logs (Ctrl+C to exit)..."
    docker-compose logs -f
}

# Stop services
stop_services() {
    echo_info "Stopping services..."
    docker-compose down
    echo_info "Services stopped successfully!"
}

# Show usage
show_usage() {
    echo "Usage: $0 [build|push|deploy|stop|all]"
    echo ""
    echo "Commands:"
    echo "  build   - Build Docker images"
    echo "  push    - Push images to Docker Hub"
    echo "  deploy  - Deploy services locally with Docker Compose"
    echo "  stop    - Stop running services"
    echo "  all     - Build, push, and deploy"
    echo ""
}

# Main
case "$1" in
    build)
        build_images
        ;;
    push)
        push_images
        ;;
    deploy)
        deploy_local
        ;;
    stop)
        stop_services
        ;;
    all)
        build_images
        push_images
        deploy_local
        ;;
    *)
        show_usage
        exit 1
        ;;
esac

