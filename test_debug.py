
try:
    print("Importing libs...")
    import torch
    import soundfile
    from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
    
    print("Libraries imported success!")
    
    print("Testing Processor load...")
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    print("Processor loaded!")

    print("Testing Model load...")
    model = SpeechT5ForTextToSpeech.from_pretrained("nayerim/speecht5-indonesian-tts")
    print("Model loaded!")

    print("Testing Vocoder load...")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
    print("Vocoder loaded!")
    
    print("✅ TEST PASSED!")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
