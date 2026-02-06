"""
VPS Voice Agent for Lentera (Standard FastAPI)
Uses OpenAI (LLM) + EdgeTTS (Text-to-Speech)
Run on VPS: uvicorn vps_voice_agent:app --host 0.0.0.0 --port 8000
"""

import os
import base64
import tempfile
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import edge_tts

app = FastAPI(title="Lentera VPS Voice Agent")

# Request Model
class ChatRequest(BaseModel):
    text: str

@app.post("/chat")
async def chat_and_speak(request: ChatRequest):
    """
    Receives: {"text": "Hello AI"}
    Returns: {"text": "Response text", "audio_base64": "..."}
    """
    user_text = request.text
    if not user_text:
        raise HTTPException(status_code=400, detail="No text provided")

    print(f"🎤 User said: {user_text}")

    # 1. Call OpenAI (LLM)
    # Ensure OPENAI_API_KEY is set in environment variables
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
         raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set on server")

    client = OpenAI(api_key=api_key)
    
    system_prompt = (
        "Kamu adalah LENTERA, teman curhat dan konselor kesehatan mental yang empatik. "
        "Jawab dengan singkat, hangat, dan mendukung (maksimal 2-3 kalimat). "
        "Gunakan bahasa Indonesia yang natural dan menenangkan."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini", # Cost effective
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        ai_text = completion.choices[0].message.content
        print(f"🤖 AI replying: {ai_text}")

    except Exception as e:
        print(f"❌ OpenAI Error: {e}")
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

    # 2. Convert to Audio (EdgeTTS)
    voice = "id-ID-ArdiNeural" 
    
    try:
        communicate = edge_tts.Communicate(ai_text, voice)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fp:
            temp_filename = fp.name
        
        await communicate.save(temp_filename)
        
        # Read file to base64
        with open(temp_filename, "rb") as f:
            audio_bytes = f.read()
            
        os.remove(temp_filename)
        
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        
        return {
            "text": ai_text,
            "audio_base64": audio_b64,
            "format": "mp3"
        }

    except Exception as e:
        print(f"❌ TTS Error: {e}")
        raise HTTPException(status_code=500, detail=f"TTS Error: {str(e)}")

@app.get("/health")
def health():
    return {"status": "ok", "service": "lentera-vps-voice-agent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
