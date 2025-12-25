"""
LENTERA Backend - FastAPI Server
Provides AI-powered mental health counseling services with voice support
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
import asyncio
import json
import base64
from typing import Optional
import os
import logging

# Import services
from ollama_service import OllamaService, MENTAL_HEALTH_SYSTEM_PROMPT
from whisper_service import get_whisper_service
from tts_service import get_tts_service
from audio_utils import AudioUtils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LENTERA Backend API",
    description="AI-powered mental health counseling backend with voice support",
    version="2.0.0"
)

# CORS middleware untuk Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk development, untuk production ganti dengan domain spesifik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ollama_service = OllamaService()
whisper_service = None
tts_service = None

# Models
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None

class VoiceResponse(BaseModel):
    transcript: str
    ai_response: str
    audio_base64: str
    confidence: float

# Startup event - initialize services
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global whisper_service, tts_service
    
    logger.info("Starting LENTERA Backend...")
    
    # Initialize Whisper
    try:
        whisper_service = get_whisper_service()
        await whisper_service.initialize()
        logger.info("✓ Whisper STT initialized")
    except Exception as e:
        logger.error(f"✗ Failed to initialize Whisper: {e}")
    
    # Initialize TTS
    try:
        tts_service = get_tts_service()
        logger.info("✓ Edge TTS initialized")
    except Exception as e:
        logger.error(f"✗ Failed to initialize TTS: {e}")
    
    # Check Ollama
    try:
        is_healthy = await ollama_service.check_health()
        if is_healthy:
            logger.info("✓ Ollama service connected")
        else:
            logger.warning("⚠ Ollama service not reachable")
    except Exception as e:
        logger.error(f"✗ Ollama check failed: {e}")
    
    logger.info("LENTERA Backend ready! 🚀")

# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "LENTERA Backend API",
        "version": "2.0.0",
        "features": ["chat", "voice", "mood_analysis"]
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check for all services"""
    ollama_healthy = await ollama_service.check_health()
    whisper_healthy = await whisper_service.health_check() if whisper_service else False
    tts_healthy = await tts_service.health_check() if tts_service else False
    
    return {
        "status": "ok" if all([ollama_healthy, whisper_healthy, tts_healthy]) else "degraded",
        "services": {
            "ollama": "ready" if ollama_healthy else "unavailable",
            "whisper": "ready" if whisper_healthy else "unavailable",
            "tts": "ready" if tts_healthy else "unavailable"
        },
        "info": {
            "whisper": whisper_service.get_info() if whisper_service else {},
            "tts": tts_service.get_info() if tts_service else {}
        }
    }

# Chat endpoint (REST API)
@app.post("/api/chat")
async def chat(message: ChatMessage):
    """
    Process text chat messages with AI
    """
    try:
        # Prepare messages for Ollama
        messages = [
            {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT},
            {"role": "user", "content": message.message}
        ]
        
        # Get response from Ollama
        response = await ollama_service.chat(messages)
        
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        
        ai_message = response.get("message", {}).get("content", "")
        
        return {
            "message": ai_message,
            "conversation_id": message.conversation_id or "new-conv-id",
            "timestamp": response.get("created_at", "")
        }
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Voice transcription endpoint (test STT)
@app.post("/api/voice/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    Transcribe audio file to text (STT test endpoint)
    """
    try:
        # Read audio file
        audio_data = await audio.read()
        
        # Validate audio
        is_valid, error = AudioUtils.validate_audio(audio_data)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)
        
        # Get audio info
        audio_info = AudioUtils.get_audio_info(audio_data)
        
        # Transcribe with Whisper
        transcript, confidence = await whisper_service.transcribe_audio(audio_data)
        
        return {
            "transcript": transcript,
            "confidence": confidence,
            "audio_info": audio_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Voice synthesis endpoint (test TTS)
@app.post("/api/voice/synthesize")
async def synthesize_speech(request: TTSRequest):
    """
    Convert text to speech (TTS test endpoint)
    """
    try:
        # Synthesize
        audio_data = await tts_service.synthesize(request.text)
        
        # Return audio as MP3
        return Response(
            content=audio_data,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )
        
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket untuk voice call
@app.websocket("/ws/voice-call")
async def voice_call_websocket(websocket: WebSocket):
    """
    WebSocket endpoint untuk real-time voice call
    Complete pipeline: Audio → STT → LLM → TTS → Audio
    """
    await websocket.accept()
    logger.info("Voice call WebSocket connected")
    
    try:
        while True:
            # Receive audio data from client
            data = await websocket.receive_bytes()
            
            logger.info(f"Received audio: {len(data)} bytes")
            
            try:
                # Step 1: Convert audio to WAV if needed
                wav_data = AudioUtils.convert_to_wav(data, "webm")
                
                # Step 2: Transcribe with Whisper (STT)
                transcript, confidence = await whisper_service.transcribe_audio(wav_data)
                logger.info(f"Transcribed: '{transcript}' (confidence: {confidence:.2f})")
                
                # Step 3: Get AI response from Ollama
                messages = [
                    {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT},
                    {"role": "user", "content": transcript}
                ]
                
                llm_response = await ollama_service.chat(messages)
                ai_text = llm_response.get("message", {}).get("content", "Maaf, saya tidak mengerti.")
                logger.info(f"AI response: '{ai_text[:50]}...'")
                
                # Step 4: Convert AI response to speech (TTS)
                audio_response = await tts_service.synthesize(ai_text)
                audio_base64 = base64.b64encode(audio_response).decode('utf-8')
                
                # Step 5: Send response back to client
                response = {
                    "type": "voice_response",
                    "transcript": transcript,
                    "ai_response": ai_text,
                    "audio_base64": audio_base64,
                    "confidence": confidence
                }
                
                await websocket.send_json(response)
                logger.info("Voice response sent")
                
            except Exception as e:
                logger.error(f"Voice pipeline error: {e}")
                error_response = {
                    "type": "error",
                    "message": f"Processing error: {str(e)}"
                }
                await websocket.send_json(error_response)
            
    except WebSocketDisconnect:
        logger.info("Client disconnected from voice call")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

# Mood analysis endpoint
@app.post("/api/mood/analyze")
async def analyze_mood(data: dict):
    """
    Analyze mood entry and provide insights using AI
    """
    try:
        # Build prompt for mood analysis
        mood_rating = data.get("mood_rating", 3)
        emotions = data.get("emotions", [])
        journal = data.get("journal", "")
        
        prompt = f"""
        Analyze this mood entry from a mental health perspective:
        
        Mood Rating: {mood_rating}/5
        Emotions: {', '.join(emotions)}
        Journal: {journal}
        
        Provide:
        1. Brief empathetic response
        2. 2-3 practical recommendations
        3. Any concerns to watch for
        
        Keep it supportive and concise.
        """
        
        messages = [
            {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        response = await ollama_service.chat(messages)
        ai_analysis = response.get("message", {}).get("content", "")
        
        return {
            "analysis": ai_analysis,
            "mood_score": mood_rating,
            "timestamp": response.get("created_at", "")
        }
        
    except Exception as e:
        logger.error(f"Mood analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

