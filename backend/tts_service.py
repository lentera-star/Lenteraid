"""
Text-to-Speech Service using Edge TTS
Optimized for VPS deployment - cloud-based, no heavy models
"""
import os
import io
import logging
from typing import Optional, List
import edge_tts
import asyncio

logger = logging.getLogger(__name__)


class TTSService:
    """
    Text-to-Speech service using Microsoft Edge TTS
    Free, high-quality, supports Indonesian
    """
    
    # Indonesian voices available in Edge TTS
    INDONESIAN_VOICES = {
        "female": "id-ID-GadisNeural",  # Female, natural
        "male": "id-ID-ArdiNeural"      # Male, natural
    }
    
    def __init__(
        self,
        voice: str = "id-ID-GadisNeural",
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz"
    ):
        """
        Initialize TTS service
        
        Args:
            voice: Voice ID (use INDONESIAN_VOICES)
            rate: Speech rate (-50% to +100%)
            volume: Volume (-50% to +50%)
            pitch: Pitch adjustment
        """
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.pitch = pitch
        
        logger.info(f"TTSService initialized: voice={voice}")
    
    async def synthesize(
        self,
        text: str,
        output_format: str = "audio-24khz-48kbitrate-mono-mp3"
    ) -> bytes:
        """
        Convert text to speech
        
        Args:
            text: Text to synthesize
            output_format: Audio format (mp3, wav, etc.)
        
        Returns:
            Audio data as bytes
        """
        try:
            logger.info(f"Synthesizing text: '{text[:50]}...'")
            
            # Create TTS communicator
            communicate = edge_tts.Communicate(
                text=text,
                voice=self.voice,
                rate=self.rate,
                volume=self.volume,
                pitch=self.pitch
            )
            
            # Collect audio chunks
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            
            logger.info(f"Synthesized {len(audio_data)} bytes of audio")
            return audio_data
            
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            raise
    
    async def synthesize_to_file(
        self,
        text: str,
        output_path: str
    ):
        """
        Synthesize text and save to file
        
        Args:
            text: Text to synthesize
            output_path: Output file path
        """
        try:
            audio_data = await self.synthesize(text)
            
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            
            logger.info(f"Saved audio to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save audio file: {e}")
            raise
    
    @staticmethod
    async def list_voices(language: str = "id") -> List[dict]:
        """
        List available voices for a language
        
        Args:
            language: Language code (e.g., 'id', 'en')
        
        Returns:
            List of voice information dicts
        """
        try:
            voices = await edge_tts.list_voices()
            
            # Filter by language
            filtered_voices = [
                {
                    "name": voice["ShortName"],
                    "gender": voice["Gender"],
                    "locale": voice["Locale"]
                }
                for voice in voices
                if voice["Locale"].startswith(language)
            ]
            
            return filtered_voices
            
        except Exception as e:
            logger.error(f"Failed to list voices: {e}")
            return []
    
    async def health_check(self) -> bool:
        """Check if TTS service is working"""
        try:
            # Try to synthesize a short test
            test_audio = await self.synthesize("Test")
            return len(test_audio) > 0
        except Exception as e:
            logger.error(f"TTS health check failed: {e}")
            return False
    
    def get_info(self) -> dict:
        """Get service information"""
        return {
            "service": "Edge TTS",
            "voice": self.voice,
            "rate": self.rate,
            "volume": self.volume,
            "pitch": self.pitch,
            "available_voices": self.INDONESIAN_VOICES
        }


# Global instance (singleton)
tts_service: Optional[TTSService] = None


def get_tts_service() -> TTSService:
    """Get or create TTS service instance"""
    global tts_service
    
    if tts_service is None:
        voice = os.getenv("TTS_VOICE", "id-ID-GadisNeural")
        rate = os.getenv("TTS_RATE", "+0%")
        volume = os.getenv("TTS_VOLUME", "+0%")
        pitch = os.getenv("TTS_PITCH", "+0Hz")
        
        tts_service = TTSService(
            voice=voice,
            rate=rate,
            volume=volume,
            pitch=pitch
        )
    
    return tts_service
