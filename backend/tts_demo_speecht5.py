"""
TTS Demo: SpeechT5-Indonesian
Generate samples using SpeechT5 fine-tuned for Indonesian
"""

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
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
    """Load SpeechT5-Indonesian model and speaker embeddings"""
    print("[*] Loading SpeechT5-Indonesian model...")
    
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("nayerim/speecht5-indonesian-tts")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
    
    print("[*] Loading speaker embeddings (CMU Arctic)...")
    try:
        # Load x-vector embeddings dataset
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        print(f"[+] Embeddings loaded! Total samples: {len(embeddings_dataset)}")
    except Exception as e:
        print(f"[!] Warning: Could not load embeddings: {e}")
        embeddings_dataset = None
    
    print("[+] Model & Embeddings loaded!")
    return processor, model, vocoder, embeddings_dataset

def generate_speech(text: str, processor, model, vocoder, embeddings_dataset=None, speaker_id=6799):
    """Generate speech from text"""
    inputs = processor(text=text, return_tensors="pt")
    
    # Use valid speaker embedding
    if embeddings_dataset is not None:
        try:
            # Try specific index (6799 is 'slt' female - VERY STABLE in most demos)
            # Index 7306 is 'rms' male
            # Let's force 6799 first to get ANY clear audio
            idx = speaker_id if speaker_id < len(embeddings_dataset) else 6799
            
            emb_tensor = torch.tensor(embeddings_dataset[idx]["xvector"])
            
            # CRITICALLY IMPORTANT: Normalize embedding!
            # SpeechT5 is sensitive to magnitude.
            emb_tensor = torch.nn.functional.normalize(emb_tensor, dim=-1)
            
            speaker_embeddings = emb_tensor.unsqueeze(0)
            print(f"   [i] Using Speaker Index: {idx}")
        except Exception as e:
             print(f"   [!] Error selecting speaker: {e}. Falling back to random (NOISE).")
             speaker_embeddings = torch.randn(1, 512)
    else:
        print("   [!] No embeddings dataset. Using random (Expect NOISE)")
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
    print("   SPEECHT5-INDONESIAN Demo")
    print("="*70)
    
    # Setup
    processor, model, vocoder, speaker_emb = setup_model()
    output_dir = Path("tts_demo_speecht5")
    output_dir.mkdir(exist_ok=True)
    
    for i, text in enumerate(TEST_TEXTS, 1):
        print(f"\n[*] Generating sample {i}...")
        print(f"   Text: {text[:50]}...")
        
        # Generate speech
        audio = generate_speech(text, processor, model, vocoder, speaker_emb)
        
        # Save as WAV
        output_file = output_dir / f"sample_{i}.wav"
        sf.write(str(output_file), audio, samplerate=16000)
        print(f"   [+] Saved: {output_file}")
    
    print("\n" + "="*70)
    print("[+] SpeechT5 samples generated!")
    print(f"Location: {output_dir.absolute()}")
    print("="*70)

if __name__ == "__main__":
    main()
