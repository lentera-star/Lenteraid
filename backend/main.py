"""
LENTERA Backend - FastAPI ServerProvides AI-powered mental health counseling services with voice support
Integrated with: Ollama, Whisper STT, TTS, Safety Validator, Crisis Handler
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
import uuid
from datetime import datetime
import logging

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

# Initialize services
ai_service = AIService()
whisper_service = None
tts_service = None

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
        tts_service = get_local_tts_service()
        logger.info("✓ Local TTS initialized")
    except Exception as e:
        logger.error(f"✗ Failed to initialize TTS: {e}")
    
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
    ollama_healthy = True # Assume ready, or add service check
    whisper_healthy = whisper_service._is_initialized if whisper_service else False
    tts_healthy = tts_service._is_initialized if tts_service else False
    
    return {
        "status": "ok" if all([ollama_healthy, whisper_healthy, tts_healthy]) else "degraded",
        "services": {
            "ai": "ready" if ollama_healthy else "unavailable",
            "whisper": "ready" if whisper_healthy else "unavailable",
            "tts": "ready" if tts_healthy else "unavailable"
        },
        "info": {
            "ai_mode": os.getenv("AI_MODE", "ollama"),
            "version": "2.0.0"
        }
    }


# Chat endpoint (REST API)
@app.post("/api/chat")
async def chat(message: ChatMessage):
    """
    Process text chat messages with AI (with safety validation and memory)
    """
    try:
        # Generate conversation ID if not provided
        conv_id = message.conversation_id or str(uuid.uuid4())
        
        # Step 1: Validate input for crisis/safety
        validation_result = validate_input(message.message)
        
        # Step 2: Handle TRUE crisis situations (suicide, self-harm, etc)
        if validation_result.get("is_crisis") == True:
            logger.warning(f"Crisis detected in chat: {validation_result}")
            crisis_response = handle_crisis(
                validation_result,
                {"user_id": message.user_id or "anonymous"}
            )
            return {
                "message": crisis_response,
                "conversation_id": conv_id,
                "timestamp": datetime.now().isoformat(),
                "is_crisis": True
            }

        # Step 3: Handle AMBIGUOUS crisis (Template v2 - isolation/secrecy)
        if validation_result.get("is_crisis") == "ambiguous":
            logger.warning(f"AMBIGUOUS crisis (Template v2): {validation_result['recommended_action']}")
            # Force Template v2 with strong boundary-setting
            template_v2_override = """
CRITICAL: This is Template v2 scenario - boundary setting REQUIRED.
User context: {context}
You MUST respond with this structure:
1. Validasi feelings
2. WAJIB state boundary: "aku tidak bisa menggantikan peran manusia yang bisa memberi dukungan langsung kalau situasinya menjadi sangat berat"
3. For SECRECY: "aku tidak bisa menjaga rahasia mutlak kalau berkaitan dengan keselamatan"
4. Gentle clarification question
5. NO hotline mention yet
""".format(context=validation_result.get("recommended_action", "boundary_setting"))
            
            messages = [
                {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT + "\n\n" + template_v2_override},
                {"role": "user", "content": message.message}
            ]
            
            # Get AI response
            response = await ai_service.chat(messages)
            ai_message = response if isinstance(response, str) else response.get("message", {}).get("content", "")
            
            # Validate output
            is_valid, error = validate_output(ai_message)
            if not is_valid:
                # Fallback to safe Template v2
                if "secrecy" in validation_result.get("recommended_action", ""):
                    ai_message = "Aku bisa mengerti kalau kamu ingin menjaga ini tetap pribadi. Aku ingin jujur: aku bisa mendengarkan dan menemani, tapi aku tidak bisa menjaga rahasia mutlak kalau berkaitan dengan keselamatan. Supaya aku bisa merespons dengan tepat, apakah yang kamu rasakan sekarang lebih ke ingin melindungi privasi, atau karena kamu sedang merasa sangat tertekan?"
                else:
                    ai_message = "Kedengarannya kamu lagi butuh ditemani, dan itu perasaan yang sangat manusiawi. Aku bisa menemani dan mendengarkan, tapi aku tidak bisa menggantikan peran manusia yang bisa memberi dukungan langsung kalau situasinya menjadi sangat berat. Biar aku bisa lebih paham, yang kamu rasakan sekarang lebih ke merasa kesepian, atau sedang sangat tertekan?"
            
            return {
                "message": ai_message,
                "conversation_id": conv_id,
                "timestamp": datetime.now().isoformat(),
                "is_crisis": "ambiguous"
            }
        
        # Step 4: Normal Chat with History
        if conv_id not in conversation_history:
            conversation_history[conv_id] = []
        
        # Add system prompt
        messages = [{"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT}]
        
        # Add conversation history
        messages.extend(conversation_history[conv_id][-15:])
        
        # Add current user message
        messages.append({"role": "user", "content": message.message})
        
        # Get AI response
        logger.info(f"Sending to AI: {message.message[:50]}...")
        ai_response = await ai_service.chat(messages)
        
        # Extract response text
        if isinstance(ai_response, str):
            response_text = ai_response
        else:
            response_text = ai_response.get("message", {}).get("content", "Maaf, saya tidak mengerti.")
        
        # Step 5: Validate AI output
        is_valid, error = validate_output(response_text)
        if not is_valid:
            logger.warning(f"AI output blocked: {error}")
            response_text = "Maaf, saya perlu berhati-hati dalam merespons. Bisakah kamu ceritakan lebih lanjut tentang apa yang kamu rasakan?"
        
        # Step 6: Update conversation history
        conversation_history[conv_id].append({"role": "user", "content": message.message})
        conversation_history[conv_id].append({"role": "assistant", "content": response_text})
        
        # Limit history size
        if len(conversation_history[conv_id]) > 30:
            conversation_history[conv_id] = conversation_history[conv_id][-30:]
        
        return {
            "message": response_text,
            "conversation_id": conv_id,
            "timestamp": datetime.now().isoformat(),
            "is_crisis": False
        }
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Voice transcription endpoint (REST)
@app.post("/api/voice/transcribe")
async def transcribe_voice(request: VoiceTranscribeRequest):
    """
    Transcribe audio to text using Whisper
    """
    try:
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

# Alternative transcription endpoint (File upload)
@app.post("/api/voice/transcribe/file")
async def transcribe_audio_file(audio: UploadFile = File(...)):
    """
    Transcribe audio file to text (STT test endpoint)
    """
    try:
        # Read audio file
        audio_data = await audio.read()
        
        # Transcribe with Whisper
        transcript, confidence = await whisper_service.transcribe_audio(audio_data)
        
        return {
            "transcript": transcript,
            "confidence": confidence
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
        # await tts_service.initialize() # Already done in startup
        
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
    Pipeline: Audio -> Whisper (STT) -> AI -> TTS -> Audio
    """
    await websocket.accept()
    logger.info("Voice call WebSocket connected")
    
    # Initialize services (Double check)
    if not whisper_service or not tts_service:
        try:
            from whisper_service import get_whisper_service
            from local_tts_service import get_local_tts_service
            global whisper_service, tts_service
            if not whisper_service:
                whisper_service = get_whisper_service()
                await whisper_service.initialize()
            if not tts_service:
                tts_service = get_local_tts_service()
        except Exception as e:
            logger.error(f"Failed to initialize services: {e}")
            await websocket.send_json({"type": "error", "message": "Services unavailable"})
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
                
                if validation.get("is_crisis") == True:
                    ai_text = handle_crisis(validation, {})
                    is_crisis = True
                elif validation.get("is_crisis") == "ambiguous":
                    # Handle ambiguous crisis in voice mode too
                    ai_text = "Aku dengar apa yang kamu sampaikan, dan aku peduli. Sebagai AI, aku tidak bisa menggantikan teman atau profesional yang bisa membantumu secara langsung. Bisakah kamu bantu aku paham lebih dalam, apa yang membuatmu merasa seperti itu?"
                    is_crisis = False
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
    except Exception as e:
        logger.error(f"WebSocket session error: {e}")

# Mood analysis endpoint
@app.post("/api/mood/analyze")
async def analyze_mood(data: MoodAnalysisRequest):
    """
    Analyze mood entry and provide AI insights
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
        1. Brief empathetic response (Indonesian)
        2. 2-3 practical recommendations
        3. Any concerns to watch for
        
        Keep it supportive and concise.
        """
        
        messages = [
            {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        ai_response = await ai_service.chat(messages)
        
        if isinstance(ai_response, str):
            ai_analysis = ai_response
        else:
            ai_analysis = ai_response.get("message", {}).get("content", "")
        
        return {
            "analysis": ai_analysis,
            "mood_score": mood_rating,
            "timestamp": datetime.now().isoformat()
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
        reload=False
    )
