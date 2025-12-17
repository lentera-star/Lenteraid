"""
LENTERA Backend - FastAPI Server
Provides AI-powered mental health counseling services
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
from typing import Optional
import os

app = FastAPI(
    title="LENTERA Backend API",
    description="AI-powered mental health counseling backend",
    version="1.0.0"
)

# CORS middleware untuk Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk development, untuk production ganti dengan domain spesifik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None

class VoiceCallRequest(BaseModel):
    user_id: str
    audio_data: bytes

# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "LENTERA Backend API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "ollama": "ready",  # TODO: Check actual Ollama connection
        "whisper": "ready",  # TODO: Check actual Whisper connection
        "tts": "ready"  # TODO: Check actual TTS connection
    }

# Chat endpoint (REST API)
@app.post("/api/chat")
async def chat(message: ChatMessage):
    """
    Process text chat messages with AI
    """
    # TODO: Integrate with Ollama
    response = {
        "message": f"AI Response to: {message.message}",
        "conversation_id": message.conversation_id or "new-conv-id",
        "timestamp": "2025-12-16T16:20:00Z"
    }
    return response

# WebSocket untuk voice call
@app.websocket("/ws/voice-call")
async def voice_call_websocket(websocket: WebSocket):
    """
    WebSocket endpoint untuk real-time voice call
    Handles bidirectional audio streaming
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive audio data from client
            data = await websocket.receive_bytes()
            
            # TODO: Process dengan Whisper (STT)
            # TODO: Process dengan Ollama (LLM)
            # TODO: Process dengan TTS
            
            # Send response audio back
            response = {
                "type": "audio",
                "data": "base64_encoded_audio_response",
                "transcript": "AI response transcript"
            }
            await websocket.send_json(response)
            
    except WebSocketDisconnect:
        print("Client disconnected from voice call")

# Mood analysis endpoint
@app.post("/api/mood/analyze")
async def analyze_mood(data: dict):
    """
    Analyze mood entry and provide insights
    """
    # TODO: Integrate with Ollama for mood analysis
    return {
        "insights": "Sample mood insight",
        "recommendations": ["Take a walk", "Practice deep breathing"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
