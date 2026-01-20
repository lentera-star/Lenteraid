"""
TTS Demo: SpeechT5-Indonesian
Generate samples using SpeechT5 fine-tuned for Indonesian
"""

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch
import soundfile as sf
from pathlib import Path
import numpy as np

# Test texts (same as Edge TTS for comparison)
TEST_TEXTS = [
    "Halo, aku LENTERA, asisten mental health kamu. Bagaimana perasaan kamu hari ini?",
    "Aku mendengar kamu sedang merasa stress dengan kuliah. Cerita aja, aku di sini untuk mendengarkan.",
    "Kamu tidak sendirian dalam menghadapi ini. Yuk, kita coba cari solusi bersama."
]

def setup_model():
    """Load SpeechT5-Indonesian model"""
    print("📦 Loading SpeechT5-Indonesian model...")
    
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("nayerim/speecht5-indonesian-tts")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
    
    # Load speaker embeddings (default)
    # Note: You can customize voice by providing different embeddings
    embeddings_dataset = torch.load("spkemb.pt") if Path("spkemb.pt").exists() else None
    
    print("✅ Model loaded!")
    return processor, model, vocoder, embeddings_dataset

def generate_speech(text: str, processor, model, vocoder, speaker_embeddings=None):
    """Generate speech from text"""
    inputs = processor(text=text, return_tensors="pt")
    
    # Use default speaker embedding if not provided
    if speaker_embeddings is None:
        # Create a default random embedding
        speaker_embeddings = torch.randn(1, 512)
    
    with torch.no_grad():
        speech = model.generate_speech(
            inputs["input_ids"],
            speaker_embeddings,
            vocoder=vocoder
        )
    
    return speech.numpy()

def main():
    print("="*70)
    print("🎙️ SPEECHT5-INDONESIAN Demo")
    print("="*70)
    
    # Setup
    processor, model, vocoder, speaker_emb = setup_model()
    output_dir = Path("tts_demo_speecht5")
    output_dir.mkdir(exist_ok=True)
    
    for i, text in enumerate(TEST_TEXTS, 1):
        print(f"\n📝 Generating sample {i}...")
        print(f"   Text: {text[:50]}...")
        
        # Generate speech
        audio = generate_speech(text, processor, model, vocoder, speaker_emb)
        
        # Save as WAV
        output_file = output_dir / f"sample_{i}.wav"
        sf.write(str(output_file), audio, samplerate=16000)
        print(f"   ✅ Saved: {output_file}")
    
    print("\n" + "="*70)
    print("✅ SpeechT5 samples generated!")
    print(f"📁 Location: {output_dir.absolute()}")
    print("="*70)

if __name__ == "__main__":
    main()
