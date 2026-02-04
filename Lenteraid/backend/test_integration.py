"""
Integration Test Script for LENTERA Backend
Tests all endpoints and services
"""
import asyncio
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from ai_service import AIService
from whisper_service import get_whisper_service
from tts_service import get_tts_service
from prompts import MENTAL_HEALTH_SYSTEM_PROMPT

async def test_ai_service():
    """Test AI service (Ollama/OpenAI)"""
    print("\n" + "="*50)
    print("Testing AI Service...")
    print("="*50)
    
    try:
        ai = AIService()
        
        # Test chat
        messages = [
            {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT},
            {"role": "user", "content": "Halo, aku sedang stress"}
        ]
        
        print("Sending chat message...")
        response = await ai.chat(messages)
        
        if isinstance(response, str):
            print(f"✓ AI Response: {response[:100]}...")
        else:
            print(f"✓ AI Response: {response.get('message', {}).get('content', '')[:100]}...")
        
        return True
    except Exception as e:
        print(f"✗ AI Service test failed: {e}")
        return False

async def test_whisper_service():
    """Test Whisper STT service"""
    print("\n" + "="*50)
    print("Testing Whisper STT...")
    print("="*50)
    
    try:
        whisper = get_whisper_service()
        
        print("Initializing Whisper...")
        await whisper.initialize()
        
        print("Checking health...")
        is_healthy = await whisper.health_check()
        
        if is_healthy:
            print("✓ Whisper is healthy")
            print(f"  Model: {whisper.model_size}")
            print(f"  Device: {whisper.device}")
            print(f"  Language: {whisper.language}")
            return True
        else:
            print("✗ Whisper health check failed")
            return False
            
    except Exception as e:
        print(f"✗ Whisper test failed: {e}")
        return False

async def test_tts_service():
    """Test TTS service"""
    print("\n" + "="*50)
    print("Testing TTS (Edge TTS)...")
    print("="*50)
    
    try:
        tts = get_tts_service()
        
        print("Checking health...")
        is_healthy = await tts.health_check()
        
        if is_healthy:
            print("✓ TTS is healthy")
            info = tts.get_info()
            print(f"  Voice: {info['voice']}")
            print(f"  Service: {info['service']}")
            return True
        else:
            print("✗ TTS health check failed")
            return False
            
    except Exception as e:
        print(f"✗ TTS test failed: {e}")
        return False

async def test_voice_pipeline():
    """Test complete voice pipeline (if test.mp3 exists)"""
    print("\n" + "="*50)
    print("Testing Voice Pipeline...")
    print("="*50)
    
    test_audio = Path("../test.mp3")
    
    if not test_audio.exists():
        print("⚠ test.mp3 not found, skipping pipeline test")
        return None
    
    try:
        whisper = get_whisper_service()
        ai = AIService()
        tts = get_tts_service()
        
        # Initialize
        await whisper.initialize()
        
        # Step 1: STT
        print("Step 1: Transcribing audio...")
        with open(test_audio, 'rb') as f:
            audio_data = f.read()
        
        transcript, confidence = await whisper.transcribe_audio(audio_data)
        print(f"✓ Transcript: '{transcript}' (confidence: {confidence:.2f})")
        
        # Step 2: LLM
        print("Step 2: Getting AI response...")
        messages = [
            {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT},
            {"role": "user", "content": transcript}
        ]
        
        response = await ai.chat(messages)
        ai_text = response if isinstance(response, str) else response.get('message', {}).get('content', '')
        print(f"✓ AI Response: '{ai_text[:50]}...'")
        
        # Step 3: TTS
        print("Step 3: Synthesizing speech...")
        audio_bytes = await tts.synthesize(ai_text)
        print(f"✓ Generated {len(audio_bytes)} bytes of audio")
        
        # Save test output
        output_path = Path("test_output.mp3")
        with open(output_path, 'wb') as f:
            f.write(audio_bytes)
        print(f"✓ Saved to {output_path}")
        
        print("\n🎉 Voice pipeline test PASSED!")
        return True
        
    except Exception as e:
        print(f"✗ Voice pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all integration tests"""
    print("\n" + "="*70)
    print(" LENTERA BACKEND INTEGRATION TESTS")
    print("="*70)
    
    results = {}
    
    # Test individual services
    results['ai'] = await test_ai_service()
    results['whisper'] = await test_whisper_service()
    results['tts'] = await test_tts_service()
    
    # Test complete pipeline
    pipeline_result = await test_voice_pipeline()
    if pipeline_result is not None:
        results['pipeline'] = pipeline_result
    
    # Summary
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    
    for service, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{service.upper():15} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Backend is ready for integration.")
    else:
        print("⚠ Some tests failed. Please fix issues before proceeding.")
    print("="*70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
