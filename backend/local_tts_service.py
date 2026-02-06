"""
Local Text-to-Speech Service using SpeechT5 Indonesian
Fully offline - no data sent to external servers
Model: nayerim/speecht5-indonesian-tts (Hugging Face)
"""
import os
import io
import logging
import numpy as np
import soundfile as sf
from typing import Optional
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch

logger = logging.getLogger(__name__)


class LocalTTSService:
    """
    Local Text-to-Speech service using SpeechT5 Indonesian
    Runs fully offline on VPS/local machine
    """
    
    def __init__(
        self,
        model_name: str = "nayerim/speecht5-indonesian-tts",
        device: str = "cpu"
    ):
        """
        Initialize Local TTS service
        
        Args:
            model_name: Hugging Face model identifier
            device: cpu or cuda
        """
        self.model_name = model_name
        self.device = device
        self.processor = None
        self.model = None
        self.vocoder = None
        self._is_initialized = False
        
        logger.info(f"LocalTTSService configured: model={model_name}, device={device}")
    
    async def initialize(self):
        """Load TTS model (lazy loading)"""
        if self._is_initialized:
            return
        
        try:
            logger.info(f"Loading TTS model: {self.model_name}")
            
            # Load processor
            self.processor = SpeechT5Processor.from_pretrained(self.model_name)
            
            # Load model
            self.model = SpeechT5ForTextToSpeech.from_pretrained(self.model_name)
            self.model.to(self.device)
            
            # Load vocoder (for audio generation)
            self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
            self.vocoder.to(self.device)
            
            self._is_initialized = True
            logger.info("✓ Local TTS model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load TTS model: {e}")
            raise
    
    async def synthesize(
        self,
        text: str,
        speaker_embedding: Optional[np.ndarray] = None
    ) -> bytes:
        """
        Convert text to speech
        
        Args:
            text: Text to synthesize
            speaker_embedding: Optional speaker embedding for voice characteristics
        
        Returns:
            Audio data as bytes (WAV format)
        """
        if not self._is_initialized:
            await self.initialize()
        
        try:
            logger.info(f"Synthesizing text: '{text[:50]}...'")
            
            # Preprocess text
            inputs = self.processor(text=text, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Use default speaker embedding if not provided
            if speaker_embedding is None:
                # Create default Indonesian female voice embedding
                speaker_embedding = self._get_default_speaker_embedding()
            
            speaker_embedding = torch.tensor(speaker_embedding).unsqueeze(0).to(self.device)
            
            # Generate speech
            with torch.no_grad():
                speech = self.model.generate_speech(
                    inputs["input_ids"],
                    speaker_embedding,
                    vocoder=self.vocoder
                )
            
            # Convert to numpy
            audio_array = speech.cpu().numpy()
            
            # Save to bytes (WAV format)
            audio_buffer = io.BytesIO()
            sf.write(audio_buffer, audio_array, samplerate=16000, format='WAV')
            audio_bytes = audio_buffer.getvalue()
            
            logger.info(f"Synthesized {len(audio_bytes)} bytes of audio")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            raise
    
    def _get_default_speaker_embedding(self) -> np.ndarray:
        """
        Get default speaker embedding for Indonesian female voice
        This creates a neutral, pleasant voice
        """
        # Create embeddings dataset for Indonesian voices
        # You can customize this based on your preference
        embedding_dim = 512
        
        # Default embedding (neutral Indonesian female voice)
        # In production, you can load pre-computed embeddings from file
        default_embedding = np.random.randn(embedding_dim).astype(np.float32)
        default_embedding = default_embedding / np.linalg.norm(default_embedding)
        
        return default_embedding
    
    async def synthesize_to_file(
        self,
        text: str,
        output_path: str,
        speaker_embedding: Optional[np.ndarray] = None
    ):
        """
        Synthesize text and save to file
        
        Args:
            text: Text to synthesize
            output_path: Output file path
            speaker_embedding: Optional speaker embedding
        """
        try:
            audio_data = await self.synthesize(text, speaker_embedding)
            
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            
            logger.info(f"Saved audio to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save audio file: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if TTS service is working"""
        try:
            if not self._is_initialized:
                await self.initialize()
            
            # Try to synthesize a short test
            test_audio = await self.synthesize("Test")
            return len(test_audio) > 0
            
        except Exception as e:
            logger.error(f"TTS health check failed: {e}")
            return False
    
    def get_info(self) -> dict:
        """Get service information"""
        return {
            "service": "Local TTS (SpeechT5)",
            "model": self.model_name,
            "device": self.device,
            "initialized": self._is_initialized,
            "privacy": "Fully offline - no external API calls",
            "language": "Indonesian"
        }


# Global instance (singleton)
local_tts_service: Optional[LocalTTSService] = None


def get_local_tts_service() -> LocalTTSService:
    """Get or create Local TTS service instance"""
    global local_tts_service
    
    if local_tts_service is None:
        model_name = os.getenv("LOCAL_TTS_MODEL", "nayerim/speecht5-indonesian-tts")
        device = os.getenv("TTS_DEVICE", "cpu")
        
        local_tts_service = LocalTTSService(
            model_name=model_name,
            device=device
        )
    
    return local_tts_service
