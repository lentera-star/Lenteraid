"""
Audio utility functions for voice processing
Handles format conversion, validation, and preprocessing
"""
import io
import os
import logging
from typing import Optional, Tuple
from pydub import AudioSegment
import numpy as np

logger = logging.getLogger(__name__)


class AudioUtils:
    """Utility functions for audio processing"""
    
    # Target sample rate for Whisper
    TARGET_SAMPLE_RATE = 16000
    
    # Supported input formats
    SUPPORTED_FORMATS = ["wav", "mp3", "ogg", "webm", "m4a", "flac"]
    
    # Max audio length (5 minutes)
    MAX_DURATION_SECONDS = 300
    
    @staticmethod
    def convert_to_wav(
        audio_data: bytes,
        input_format: str = "webm"
    ) -> bytes:
        """
        Convert audio to WAV format suitable for Whisper
        
        Args:
            audio_data: Input audio bytes
            input_format: Input format (webm, mp3, ogg, etc.)
        
        Returns:
            WAV audio bytes
        """
        try:
            # Load audio
            audio = AudioSegment.from_file(
                io.BytesIO(audio_data),
                format=input_format
            )
            
            # Convert to mono if stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Resample to 16kHz (Whisper's expected rate)
            if audio.frame_rate != AudioUtils.TARGET_SAMPLE_RATE:
                audio = audio.set_frame_rate(AudioUtils.TARGET_SAMPLE_RATE)
            
            # Export as WAV
            wav_buffer = io.BytesIO()
            audio.export(
                wav_buffer,
                format="wav",
                parameters=["-ar", str(AudioUtils.TARGET_SAMPLE_RATE)]
            )
            
            wav_data = wav_buffer.getvalue()
            logger.info(f"Converted {input_format} to WAV: {len(wav_data)} bytes")
            
            return wav_data
            
        except Exception as e:
            logger.error(f"Audio conversion failed: {e}")
            raise
    
    @staticmethod
    def validate_audio(
        audio_data: bytes,
        max_duration: Optional[int] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate audio data
        
        Args:
            audio_data: Audio bytes to validate
            max_duration: Maximum duration in seconds
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Try to load audio
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            # Check duration
            duration_seconds = len(audio) / 1000.0
            max_dur = max_duration or AudioUtils.MAX_DURATION_SECONDS
            
            if duration_seconds > max_dur:
                return False, f"Audio too long: {duration_seconds:.1f}s > {max_dur}s"
            
            if duration_seconds < 0.1:
                return False, "Audio too short: must be at least 0.1 seconds"
            
            # Check if audio has content
            if audio.dBFS == float('-inf'):
                return False, "Audio is silent"
            
            return True, None
            
        except Exception as e:
            return False, f"Invalid audio format: {str(e)}"
    
    @staticmethod
    def get_audio_info(audio_data: bytes) -> dict:
        """
        Get audio file information
        
        Args:
            audio_data: Audio bytes
        
        Returns:
            Dictionary with audio info
        """
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            return {
                "duration_seconds": len(audio) / 1000.0,
                "channels": audio.channels,
                "sample_rate": audio.frame_rate,
                "sample_width": audio.sample_width,
                "format": audio.format if hasattr(audio, 'format') else "unknown",
                "dBFS": audio.dBFS
            }
            
        except Exception as e:
            logger.error(f"Failed to get audio info: {e}")
            return {}
    
    @staticmethod
    def trim_silence(
        audio_data: bytes,
        silence_threshold: int = -40,
        chunk_size: int = 10
    ) -> bytes:
        """
        Trim silence from beginning and end of audio
        
        Args:
            audio_data: Input audio bytes
            silence_threshold: Silence threshold in dBFS
            chunk_size: Chunk size in milliseconds
        
        Returns:
            Trimmed audio bytes
        """
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            # Detect non-silent chunks
            non_silent_chunks = [
                chunk for chunk in audio[::chunk_size]
                if chunk.dBFS > silence_threshold
            ]
            
            if not non_silent_chunks:
                logger.warning("Audio is all silence after trimming")
                return audio_data
            
            # Trim
            trimmed = AudioSegment.silent(duration=0)
            for chunk in non_silent_chunks:
                trimmed += chunk
            
            # Export
            buffer = io.BytesIO()
            trimmed.export(buffer, format="wav")
            
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Failed to trim silence: {e}")
            return audio_data
    
    @staticmethod
    def normalize_volume(audio_data: bytes, target_dBFS: float = -20.0) -> bytes:
        """
        Normalize audio volume
        
        Args:
            audio_data: Input audio bytes
            target_dBFS: Target volume in dBFS
        
        Returns:
            Normalized audio bytes
        """
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            # Calculate gain needed
            change_in_dBFS = target_dBFS - audio.dBFS
            
            # Apply gain
            normalized = audio.apply_gain(change_in_dBFS)
            
            # Export
            buffer = io.BytesIO()
            normalized.export(buffer, format="wav")
            
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Failed to normalize volume: {e}")
            return audio_data
