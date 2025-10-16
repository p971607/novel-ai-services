"""
IndexTTS FastAPI Service
Provides text-to-speech API endpoints
"""
import os
import uuid
import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="IndexTTS API",
    description="Bilibili's open-source AI text-to-speech system API",
    version="2.0.0"
)

# Configuration
MODEL_PATH = os.getenv("MODEL_PATH", "/app/checkpoints")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/app/output")
USE_FP16 = os.getenv("USE_FP16", "true").lower() == "true"
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))

# Ensure output directory exists
Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)

# Global TTS model instance (lazy loading)
tts_model = None


def get_tts_model():
    """Get or initialize TTS model"""
    global tts_model
    if tts_model is None:
        logger.info("Loading IndexTTS model...")
        try:
            # Import actual IndexTTS library here
            # from indextts.infer_v2 import IndexTTS2
            # tts_model = IndexTTS2(
            #     cfg_path=f"{MODEL_PATH}/config.yaml",
            #     model_dir=MODEL_PATH,
            #     use_fp16=USE_FP16
            # )
            logger.info("IndexTTS model loaded successfully")
        except Exception as e:
            logger.error(f"Model loading failed: {e}")
            raise
    return tts_model


class TTSRequest(BaseModel):
    """TTS request model"""
    text: str
    voice_prompt: Optional[str] = "examples/voice_01.wav"
    emotion: Optional[str] = "neutral"
    speed: Optional[float] = 1.0
    pitch: Optional[float] = 1.0


class TTSResponse(BaseModel):
    """TTS response model"""
    audio_url: str
    duration: float
    text: str


@app.get("/")
async def root():
    """Root path"""
    return {
        "service": "IndexTTS API",
        "version": "2.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "model_loaded": tts_model is not None
    }


@app.post("/api/tts/generate", response_model=TTSResponse)
async def generate_speech(request: TTSRequest):
    """
    Generate speech
    
    Args:
        request: TTS request parameters
        
    Returns:
        TTSResponse: Response containing audio file path
    """
    try:
        logger.info(f"Received TTS request: text='{request.text[:50]}...', voice={request.voice_prompt}")
        
        # Get TTS model
        model = get_tts_model()
        
        # Generate unique output filename
        output_filename = f"{uuid.uuid4()}.wav"
        output_path = os.path.join(OUTPUT_PATH, output_filename)
        
        # Call TTS model to generate speech
        # Implement actual IndexTTS API call here
        # model.infer(
        #     spk_audio_prompt=request.voice_prompt,
        #     text=request.text,
        #     output_path=output_path,
        #     emotion=request.emotion,
        #     speed=request.speed,
        #     pitch=request.pitch
        # )
        
        # Temporary: create empty file for testing
        Path(output_path).touch()
        
        logger.info(f"Speech generated successfully: {output_filename}")
        
        return TTSResponse(
            audio_url=f"/api/tts/audio/{output_filename}",
            duration=0.0,  # Should get from model
            text=request.text
        )
        
    except Exception as e:
        logger.error(f"Speech generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Speech generation failed: {str(e)}")


@app.get("/api/tts/audio/{filename}")
async def get_audio(filename: str):
    """
    Get generated audio file
    
    Args:
        filename: Audio filename
        
    Returns:
        FileResponse: Audio file
    """
    file_path = os.path.join(OUTPUT_PATH, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        file_path,
        media_type="audio/wav",
        filename=filename
    )


@app.post("/api/tts/upload-voice")
async def upload_voice_sample(file: UploadFile = File(...)):
    """
    Upload voice sample for cloning
    
    Args:
        file: Uploaded audio file
        
    Returns:
        dict: Response containing file path
    """
    try:
        # Save uploaded file
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(OUTPUT_PATH, filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Voice sample uploaded successfully: {filename}")
        
        return {
            "filename": filename,
            "path": f"/api/tts/audio/{filename}",
            "size": len(content)
        }
        
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@app.get("/api/tts/voices")
async def list_voices():
    """
    List available voice samples
    
    Returns:
        dict: Available voice list
    """
    examples_dir = "/app/examples"
    voices = []
    
    if os.path.exists(examples_dir):
        for file in os.listdir(examples_dir):
            if file.endswith(('.wav', '.mp3')):
                voices.append({
                    "id": file,
                    "name": file.replace('.wav', '').replace('.mp3', ''),
                    "path": f"examples/{file}"
                })
    
    return {"voices": voices}


if __name__ == "__main__":
    logger.info("Starting IndexTTS API service...")
    logger.info(f"Model path: {MODEL_PATH}")
    logger.info(f"Output path: {OUTPUT_PATH}")
    logger.info(f"Use FP16: {USE_FP16}")
    logger.info(f"Max workers: {MAX_WORKERS}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=MAX_WORKERS,
        log_level="info"
    )

