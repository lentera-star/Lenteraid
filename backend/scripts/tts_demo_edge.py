"""
TTS Demo: Edge TTS vs SpeechT5-Indonesian
Quick comparison of both TTS systems
"""

import asyncio
import edge_tts
from pathlib import Path

# Test text (mental health context)
TEST_TEXTS = [
    "Halo, aku LENTERA, asisten mental health kamu. Bagaimana perasaan kamu hari ini?",
    "Aku mendengar kamu sedang merasa stress dengan kuliah. Cerita aja, aku di sini untuk mendengarkan.",
    "Kamu tidak sendirian dalam menghadapi ini. Yuk, kita coba cari solusi bersama."
]

# Edge TTS voices for Indonesian
VOICES = {
    "male": "id-ID-ArdiNeural",
    "female": "id-ID-GadisNeural"
}

async def generate_edge_tts(text: str, voice: str, output_file: str):
    """Generate audio using Edge TTS"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"✅ Saved: {output_file}")

async def main():
    print("="*70)
    print("🎙️ EDGE TTS Demo - Indonesian Voices")
    print("="*70)
    
    output_dir = Path("tts_demo_edge")
    output_dir.mkdir(exist_ok=True)
    
    for i, text in enumerate(TEST_TEXTS, 1):
        print(f"\n📝 Text {i}: {text[:50]}...")
        
        # Generate male voice
        male_file = output_dir / f"sample_{i}_male.mp3"
        await generate_edge_tts(text, VOICES["male"], str(male_file))
        
        # Generate female voice
        female_file = output_dir / f"sample_{i}_female.mp3"
        await generate_edge_tts(text, VOICES["female"], str(female_file))
    
    print("\n" + "="*70)
    print("✅ Edge TTS samples generated!")
    print(f"📁 Location: {output_dir.absolute()}")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
