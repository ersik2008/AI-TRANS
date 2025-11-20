"""
Speech-to-text service using faster-whisper
"""
import logging
from pathlib import Path
from typing import List, Tuple
from app.models.job import Segment
import subprocess
import json

logger = logging.getLogger(__name__)

class SpeechToTextService:
    """Service for extracting text from audio/video"""
    
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.initialized = False
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize faster-whisper model"""
        try:
            # Import here to avoid loading if not needed
            from faster_whisper import WhisperModel
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
            self.initialized = True
            logger.info(f"Loaded Whisper model: {self.model_size}")
        except Exception as e:
            logger.error(f"Failed to initialize Whisper model: {e}")
            self.model = None
    
    def extract_text(self, file_path: str) -> Tuple[str, List[Segment]]:
        """
        Extract text from audio/video file
        
        Args:
            file_path: Path to media file
            
        Returns:
            Tuple of (full_text, segments)
        """
        if not self.initialized or self.model is None:
            raise RuntimeError("Whisper model not initialized")
        
        try:
            logger.info(f"Starting speech-to-text for: {file_path}")
            
            # Extract audio if video
            audio_path = self._extract_audio_if_needed(file_path)
            
            # Run Whisper
            segments_raw, info = self.model.transcribe(audio_path, language=None)
            
            segments = []
            full_text = []
            
            for segment in segments_raw:
                seg = Segment(
                    start=segment.start,
                    end=segment.end,
                    text=segment.text.strip()
                )
                segments.append(seg)
                full_text.append(seg.text)
            
            full_text_str = " ".join(full_text)
            logger.info(f"Extracted {len(segments)} segments, total text length: {len(full_text_str)}")
            
            return full_text_str, segments
            
        except Exception as e:
            logger.error(f"Error in speech-to-text: {e}")
            raise
    
    def _extract_audio_if_needed(self, file_path: str) -> str:
        """Extract audio from video if needed"""
        if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
            output_path = Path(file_path).with_suffix('.wav')
            cmd = [
                'ffmpeg', '-i', file_path, 
                '-vn', '-acodec', 'pcm_s16le', '-ar', '16000',
                '-y', str(output_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Extracted audio to: {output_path}")
            return str(output_path)
        return file_path


class MockSpeechToTextService:
    """Mock implementation for testing without GPU"""
    
    def extract_text(self, file_path: str) -> Tuple[str, List[Segment]]:
        """Return mock transcription"""
        mock_text = "This is a sample transcription of the media file."
        segments = [
            Segment(start=0.0, end=5.0, text="This is a sample"),
            Segment(start=5.0, end=10.0, text="transcription of the media file.")
        ]
        return mock_text, segments
