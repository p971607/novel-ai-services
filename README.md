# Novel AI Services

AI services deployment for novel platform: IndexTTS, ComfyUI, and Nitro proxy.

## 🚀 Services

### 1. IndexTTS
Bilibili's open-source AI text-to-speech system with zero-shot voice cloning and multiple emotions.

- **Port**: 8000
- **GPU**: Required (NVIDIA CUDA 11.8+)
- **API Endpoints**:
  - `POST /api/tts/generate` - Generate speech
  - `GET /api/tts/audio/{filename}` - Get audio file
  - `POST /api/tts/upload-voice` - Upload voice sample
  - `GET /api/tts/voices` - List available voices

### 2. ComfyUI
Powerful AI image generation tool supporting Stable Diffusion models.

- **Port**: 8001
- **GPU**: Required (NVIDIA CUDA 11.8+)
- **Web Interface**: http://localhost:8001

## 📦 Docker Images

Images are automatically built and pushed to Docker Hub via GitHub Actions:

- `p971607/index-tts:latest`
- `p971607/comfyui:latest`

## 🛠️ Local Development

### Build Images Locally

```bash
# Build IndexTTS
cd index-tts
docker build -t p971607/index-tts:latest .

# Build ComfyUI
cd comfyui
docker build -t p971607/comfyui:latest .
```

### Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Deployment

### Deploy to Xiangongyun (仙宫云)

1. **Create IndexTTS Instance**
   - Image: `p971607/index-tts:latest`
   - GPU: RTX 3090 or better
   - Port: 8000
   - Environment Variables:
     - `MODEL_PATH=/app/checkpoints`
     - `OUTPUT_PATH=/app/output`
     - `USE_FP16=true`
     - `MAX_WORKERS=4`

2. **Create ComfyUI Instance**
   - Image: `p971607/comfyui:latest`
   - GPU: RTX 3090 or better
   - Port: 8001

3. **Configure Auto-scaling**
   - Min instances: 1
   - Max instances: 5
   - Scale up threshold: CPU > 70% or GPU > 80%
   - Scale down threshold: CPU < 30% and GPU < 30%

### Deploy Nitro Proxy to Vercel

```bash
cd nitro-proxy
npm install
vercel deploy --prod
```

## 🔧 Configuration

### GitHub Secrets

Add these secrets to your GitHub repository:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password or access token

### Environment Variables

#### IndexTTS
- `MODEL_PATH`: Model files directory (default: `/app/checkpoints`)
- `OUTPUT_PATH`: Output files directory (default: `/app/output`)
- `USE_FP16`: Use FP16 precision (default: `true`)
- `MAX_WORKERS`: Maximum concurrent workers (default: `4`)

#### ComfyUI
- `COMFYUI_MODEL_PATH`: Model files directory (default: `/app/models`)
- `COMFYUI_OUTPUT_PATH`: Output files directory (default: `/app/output`)

## 📚 API Documentation

### IndexTTS API

#### Generate Speech

```bash
curl -X POST http://localhost:8000/api/tts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test.",
    "voice_prompt": "examples/voice_01.wav",
    "emotion": "neutral",
    "speed": 1.0,
    "pitch": 1.0
  }'
```

#### Upload Voice Sample

```bash
curl -X POST http://localhost:8000/api/tts/upload-voice \
  -F "file=@voice_sample.wav"
```

#### List Available Voices

```bash
curl http://localhost:8000/api/tts/voices
```

## 🏗️ Architecture

```
User → Nitro Proxy (Vercel) → AI Services (Xiangongyun)
                              ├── IndexTTS (Port 8000)
                              └── ComfyUI (Port 8001)
```

## 📝 License

MIT

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

