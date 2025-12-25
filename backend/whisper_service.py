"""
Whisper Speech-to-Text Service
Optimized for CPU deployment on VPS (Contabo)
"""
import os
import io
import logging
from typing import Optional, Tuple
from faster_whisper import WhisperModel
import numpy as np

logger = logging.getLogger(__name__)


class WhisperService:
    """
    Speech-to-Text service using faster-whisper
    Optimized for CPU-only environments
    """
    
    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8",
        language: str = "id"
    ):
        """
        Initialize Whisper service
        
        Args:
            model_size: Model size (tiny, base, small, medium)
                       Recommended for CPU: base (75MB)
            device: cpu or cuda
            compute_type: int8 (CPU optimized) or float16 (GPU)
            language: Language code (id for Indonesian)
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.language = language
        self.model = None
        self._is_initialized = False
        
        logger.info(f"WhisperService configured: model={model_size}, device={device}, language={language}")
    
    async def initialize(self):
        """Load Whisper model (lazy loading)"""
        if self._is_initialized:
            return
        
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
                download_root=os.getenv("WHISPER_MODEL_DIR", "./models/whisper")
            )
            self._is_initialized = True
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    async def transcribe_audio(
        self,
        audio_data: bytes,
        language: Optional[str] = None
    ) -> Tuple[str, float]:
        """
        Transcribe audio to text
        
        Args:
            audio_data: Audio file bytes (wav, mp3, ogg, webm)
            language: Override language (optional)
        
        Returns:
            Tuple of (transcript, confidence)
        """
        if not self._is_initialized:
            await self.initialize()
        
        try:
            # Save audio to temporary buffer
            audio_buffer = io.BytesIO(audio_data)
            
            # Transcribe
            segments, info = self.model.transcribe(
                audio_buffer,
                language=language or self.language,
                beam_size=5,  # Balance between speed and quality
                vad_filter=True,  # Voice Activity Detection
                vad_parameters=dict(
                    min_silence_duration_ms=500  # Reduce silence processing
                )
            )
            
            # Combine segments
            transcript = ""
            total_confidence = 0.0
            segment_count = 0
            
            for segment in segments:
                transcript += segment.text + " "
                # avg_logprob is the confidence (-inf to 0, closer to 0 is better)
                # Convert to 0-1 scale
                confidence = np.exp(segment.avg_logprob)
                total_confidence += confidence
                segment_count += 1
            
            transcript = transcript.strip()
            avg_confidence = total_confidence / segment_count if segment_count > 0 else 0.0
            
            logger.info(f"Transcribed: '{transcript[:50]}...' (confidence: {avg_confidence:.2f})")
            
            return transcript, avg_confidence
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    async def transcribe_file(
        self,
        file_path: str,
        language: Optional[str] = None
    ) -> Tuple[str, float]:
        """
        Transcribe audio file
        
        Args:
            file_path: Path to audio file
            language: Override language
        
        Returns:
            Tuple of (transcript, confidence)
        """
        try:
            with open(file_path, 'rb') as f:
                audio_data = f.read()
            return await self.transcribe_audio(audio_data, language)
        except Exception as e:
            logger.error(f"Failed to read audio file: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if service is healthy"""
        try:
            if not self._is_initialized:
                await self.initialize()
            return self.model is not None
        except Exception as e:
            logger.error(f"Whisper health check failed: {e}")
            return False
    
    def get_info(self) -> dict:
        """Get service information"""
        return {
            "service": "Whisper STT",
            "model_size": self.model_size,
            "device": self.device,
            "compute_type": self.compute_type,
            "language": self.language,
            "initialized": self._is_initialized
        }


# Global instance (singleton)
whisper_service: Optional[WhisperService] = None


def get_whisper_service() -> WhisperService:
    """Get or create Whisper service instance"""
    global whisper_service
    
    if whisper_service is None:
        model_size = os.getenv("WHISPER_MODEL", "base")
        device = os.getenv("WHISPER_DEVICE", "cpu")
        compute_type = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
        language = os.getenv("WHISPER_LANGUAGE", "id")
        
        whisper_service = WhisperService(
            model_size=model_size,
            device=device,
            compute_type=compute_type,
            language=language
        )
    
    return whisper_service
