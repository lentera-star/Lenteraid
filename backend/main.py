"""
LENTERA Backend - FastAPI Server
Provides AI-powered mental health counseling services
Integrated with: Ollama, Whisper STT, TTS, Safety Validator, Crisis Handler
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
from typing import Optional
import os
import uuid
from datetime import datetime
import logging
import base64

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import services
from ai_service import AIService
from safety_validator import validate_input, validate_output, get_crisis_response
from crisis_handler import handle_crisis
from prompts import MENTAL_HEALTH_SYSTEM_PROMPT
from whisper_service import get_whisper_service
from local_tts_service import get_local_tts_service

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
ai_service = AIService()
whisper_service = get_whisper_service()
tts_service = get_local_tts_service()

app = FastAPI(
    title="LENTERA Backend API",
    description="AI-powered mental health counseling backend",
    version="2.0.0"
)

# CORS middleware untuk Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversation history (in-memory, replace with DB in production)
conversation_history = {}

# Models
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None

class MoodAnalysisRequest(BaseModel):
    mood_rating: int
    emotions: list[str]
    journal: Optional[str] = ""

class VoiceTranscribeRequest(BaseModel):
    audio_base64: str
    language: Optional[str] = "id"

class VoiceSynthesizeRequest(BaseModel):
    text: str


# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "LENTERA Backend API",
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check():
    """Check status of all services"""
    ai_mode = os.getenv("AI_MODE", "ollama")
    
    # Check services
    services = {
        "ai": "ready",
        "whisper": "initializing",
        "tts": "initializing"
    }
    
    try:
        if whisper_service._is_initialized:
            services["whisper"] = "ready"
    except:
        services["whisper"] = "not_initialized"
    
    try:
        if tts_service._is_initialized:
            services["tts"] = "ready"
    except:
        services["tts"] = "not_initialized"
    
    # Determine overall status
    all_ready = all(s == "ready" for s in services.values())
    
    return {
        "status": "ok" if all_ready else "degraded",
        "services": services,
        "info": {
            "ai_mode": ai_mode,
            "version": "2.0.0"
        }
    }


# Chat endpoint (REST API)
@app.post("/api/chat")
async def chat(message: ChatMessage):
    """
    Process text chat messages with AI
    Returns AI response with safety checks
    """
    try:
        # Generate conversation ID if not provided
        conv_id = message.conversation_id or str(uuid.uuid4())
        
        # Step 1: Validate input for crisis/safety
        validation_result = validate_input(message.message)
        
        # Step 2: Handle crisis if detected
        if validation_result.get("is_crisis"):
            crisis_response = handle_crisis(
                validation_result,
                {"user_id": message.user_id}
            )
            return {
                "message": crisis_response,
                "conversation_id": conv_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "is_crisis": True
            }
        
        # Step 3: Build messages with history
        if conv_id not in conversation_history:
            conversation_history[conv_id] = []
        
        # Add system prompt if first message
        messages = [{"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT}]
        
        # Add conversation history (last 10 messages)
        messages.extend(conversation_history[conv_id][-10:])
        
        # Add current user message
        messages.append({"role": "user", "content": message.message})
        
        # Step 4: Get AI response
        logger.info(f"Sending to AI: {message.message[:50]}...")
        ai_response = await ai_service.chat(messages)
        
        # Extract response text
        if isinstance(ai_response, str):
            response_text = ai_response
        else:
            response_text = ai_response.get("message", {}).get("content", "")
        
        # Step 5: Validate AI output
        is_valid, error = validate_output(response_text)
        if not is_valid:
            logger.warning(f"AI output blocked: {error}")
            response_text = "Maaf, saya perlu berhati-hati dalam merespons. Bisakah kamu ceritakan lebih lanjut tentang apa yang kamu rasakan?"
        
        # Step 6: Update conversation history
        conversation_history[conv_id].append({"role": "user", "content": message.message})
        conversation_history[conv_id].append({"role": "assistant", "content": response_text})
        
        # Limit history size
        if len(conversation_history[conv_id]) > 20:
            conversation_history[conv_id] = conversation_history[conv_id][-20:]
        
        return {
            "message": response_text,
            "conversation_id": conv_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "is_crisis": False
        }
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Mood analysis endpoint
@app.post("/api/mood/analyze")
async def analyze_mood(data: MoodAnalysisRequest):
    """
    Analyze mood entry and provide AI insights
    """
    try:
        # Build prompt for mood analysis
        mood_prompt = f"""Analisis mood entry berikut:
- Rating mood: {data.mood_rating}/5
- Emosi yang dirasakan: {', '.join(data.emotions)}
- Catatan jurnal: {data.journal or '(tidak ada)'}

Berikan:
1. Insight singkat tentang kondisi emosional
2. 2-3 rekomendasi praktis untuk self-care
3. Kata-kata dukungan"""

        messages = [
            {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT},
            {"role": "user", "content": mood_prompt}
        ]
        
        ai_response = await ai_service.chat(messages)
        
        if isinstance(ai_response, str):
            analysis = ai_response
        else:
            analysis = ai_response.get("message", {}).get("content", "")
        
        return {
            "analysis": analysis,
            "mood_score": data.mood_rating,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(f"Mood analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Voice transcription endpoint (REST)
@app.post("/api/voice/transcribe")
async def transcribe_voice(request: VoiceTranscribeRequest):
    """
    Transcribe audio to text using Whisper
    """
    try:
        # Initialize whisper if needed
        await whisper_service.initialize()
        
        # Decode base64 audio
        audio_data = base64.b64decode(request.audio_base64)
        
        # Transcribe
        transcript, confidence = await whisper_service.transcribe_audio(
            audio_data, 
            language=request.language
        )
        
        return {
            "transcript": transcript,
            "confidence": confidence,
            "language": request.language
        }
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Voice synthesis endpoint (REST)
@app.post("/api/voice/synthesize")
async def synthesize_voice(request: VoiceSynthesizeRequest):
    """
    Convert text to speech using TTS
    """
    try:
        # Initialize TTS if needed
        await tts_service.initialize()
        
        # Synthesize
        audio_bytes = await tts_service.synthesize(request.text)
        
        # Return as base64
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        return {
            "audio_base64": audio_base64,
            "format": "wav",
            "sample_rate": 16000
        }
        
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket untuk voice call
@app.websocket("/ws/voice-call")
async def voice_call_websocket(websocket: WebSocket):
    """
    WebSocket endpoint untuk real-time voice call
    Pipeline: Audio → Whisper (STT) → AI → TTS → Audio
    """
    await websocket.accept()
    logger.info("Voice call WebSocket connected")
    
    # Initialize services
    try:
        await whisper_service.initialize()
        await tts_service.initialize()
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        await websocket.send_json({
            "type": "error",
            "message": f"Service initialization failed: {e}"
        })
        await websocket.close()
        return
    
    # Conversation history for this session
    session_history = []
    
    try:
        while True:
            # Receive audio data from client
            data = await websocket.receive_bytes()
            logger.info(f"Received audio: {len(data)} bytes")
            
            try:
                # Step 1: STT with Whisper
                transcript, confidence = await whisper_service.transcribe_audio(data)
                logger.info(f"Transcript: {transcript} (confidence: {confidence:.2f})")
                
                if not transcript.strip():
                    await websocket.send_json({
                        "type": "error",
                        "message": "Could not transcribe audio"
                    })
                    continue
                
                # Step 2: Safety check
                validation = validate_input(transcript)
                
                if validation.get("is_crisis"):
                    ai_text = handle_crisis(validation, {})
                    is_crisis = True
                else:
                    # Step 3: AI response
                    messages = [
                        {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT}
                    ]
                    messages.extend(session_history[-10:])
                    messages.append({"role": "user", "content": transcript})
                    
                    response = await ai_service.chat(messages)
                    
                    if isinstance(response, str):
                        ai_text = response
                    else:
                        ai_text = response.get("message", {}).get("content", "")
                    
                    # Update session history
                    session_history.append({"role": "user", "content": transcript})
                    session_history.append({"role": "assistant", "content": ai_text})
                    is_crisis = False
                
                # Step 4: TTS
                audio_bytes = await tts_service.synthesize(ai_text)
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                
                # Send response
                await websocket.send_json({
                    "type": "voice_response",
                    "transcript": transcript,
                    "ai_response": ai_text,
                    "audio_base64": audio_base64,
                    "confidence": confidence,
                    "is_crisis": is_crisis
                })
                
            except Exception as e:
                logger.error(f"Voice processing error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
            
    except WebSocketDisconnect:
        logger.info("Voice call WebSocket disconnected")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )

