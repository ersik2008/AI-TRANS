"""
Text-to-speech service using Coqui TTS
"""
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class TextToSpeechService:
    """Service for generating speech from text"""
    
    def __init__(self):
        self.initialized = False
        self.tts_engine = None
        self._initialize_tts()
    
    def _initialize_tts(self):
        """Initialize TTS engine"""
        try:
            from TTS.api import TTS
            self.tts_engine = TTS(model_name="tts_models/en/ljspeech/glow-tts", gpu=False)
            self.initialized = True
            logger.info("TTS engine initialized")
        except Exception as e:
            logger.warning(f"TTS initialization failed: {e}. Using mock.")
            self.initialized = False
    
    def generate_speech(self, text: str, output_path: str, lang: str = "en") -> bool:
        """
        Generate speech from text
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            lang: Language code (for future multi-lang support)
            
        Returns:
            True if successful
        """
        if not text or not text.strip():
            logger.warning("Empty text for TTS")
            return False
        
        if not self.initialized or self.tts_engine is None:
            return self._mock_generate_speech(text, output_path)
        
        try:
            logger.info(f"Generating speech for: {text[:100]}...")
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Split long text into chunks (TTS has limits)
            chunks = self._split_text(text, max_length=500)
            
            if len(chunks) == 1:
                self.tts_engine.tts_to_file(text=text, file_path=output_path)
            else:
                # Generate multiple chunks and concatenate
                import soundfile as sf
                import numpy as np
                
                all_audio = []
                for i, chunk in enumerate(chunks):
                    chunk_path = f"{output_path}.chunk_{i}"
                    self.tts_engine.tts_to_file(text=chunk, file_path=chunk_path)
                    audio, sr = sf.read(chunk_path)
                    all_audio.append(audio)
                
                # Concatenate and save
                combined_audio = np.concatenate(all_audio)
                sf.write(output_path, combined_audio, sr)
                
                # Cleanup chunks
                for i in range(len(chunks)):
                    Path(f"{output_path}.chunk_{i}").unlink(missing_ok=True)
            
            logger.info(f"Speech generated: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error in TTS: {e}")
            return False
    
    @staticmethod
    def _split_text(text: str, max_length: int = 500) -> list:
        """Split text into chunks"""
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [text]


class MockTextToSpeechService:
    """Mock TTS service for development"""
    
    def generate_speech(self, text: str, output_path: str, lang: str = "en") -> bool:
        """Create a dummy audio file"""
        try:
            import wave
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Create a simple silent audio file for testing
            sample_rate = 22050
            duration = 1
            num_samples = sample_rate * duration
            
            with wave.open(output_path, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(b'\x00' * (num_samples * 2))
            
            logger.info(f"Mock speech generated: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error in mock TTS: {e}")
            return False
