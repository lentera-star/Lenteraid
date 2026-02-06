"""
Modal Voice Agent for Lentera
Uses OpenAI (LLM) + EdgeTTS (Text-to-Speech)
CPU-only implementation for cost efficiency.
"""

import modal
import os
import io

# Define image with dependencies
voice_image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "ffmpeg")
    .pip_install(
        "openai",
        "edge-tts",
        "fastapi[standard]",
    )
)

app = modal.App("lentera-voice-agent")

@app.function(
    image=voice_image,
    secrets=[modal.Secret.from_name("openai-secret")], # User needs to set this secret in Modal
    timeout=60,
)
@modal.web_endpoint(method="POST")
async def chat_and_speak(data: dict):
    """
    Receives: {"text": "Hello AI"}
    Returns: {"text": "Response text", "audio_base64": "..."}
    """
    from openai import OpenAI
    import edge_tts
    import base64
    import tempfile

    user_text = data.get("text", "")
    if not user_text:
        return {"error": "No text provided"}

    print(f"🎤 User said: {user_text}")

    # 1. Call OpenAI (LLM)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    
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
        return {"error": f"LLM Error: {str(e)}"}

    # 2. Convert to Audio (EdgeTTS)
    # Voice options: id-ID-GadisNeural (Female), id-ID-ArdiNeural (Male)
    voice = "id-ID-ArdiNeural" 
    
    try:
        communicate = edge_tts.Communicate(ai_text, voice)
        
        # Save to memory buffer?? EdgeTTS save() writes to file.
        # We can write to a temp file then read it back.
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
        return {"error": f"TTS Error: {str(e)}"}

@app.function(image=voice_image)
@modal.web_endpoint(method="GET")
def health():
    return {"status": "ok", "service": "lentera-voice-agent"}
