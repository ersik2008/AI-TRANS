"""
Job models for tracking translation tasks
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
import uuid

class JobStatus(str, Enum):
    """Job status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileType(str, Enum):
    """Supported file types"""
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"
    TEXT = "text"  # Добавлен новый тип для текстовых файлов

@dataclass
class Segment:
    """Text segment with timing information"""
    start: float
    end: float
    text: str

@dataclass
class BoundingBox:
    """Bounding box for OCR results"""
    x: float
    y: float
    width: float
    height: float
    text: str
    confidence: float

@dataclass
class Job:
    """Translation job model"""
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: JobStatus = JobStatus.PENDING
    file_type: Optional[FileType] = None
    source_text: str = ""
    translated_text: str = ""
    target_lang: str = "en"
    
    # File paths
    file_path: str = ""
    audio_output_path: str = ""
    
    # Results
    segments: List[Segment] = field(default_factory=list)
    image_bboxes: List[BoundingBox] = field(default_factory=list)
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "job_id": self.job_id,
            "status": self.status.value,
            "file_type": self.file_type.value if self.file_type else None,
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "target_lang": self.target_lang,
            "segments": [{"start": s.start, "end": s.end, "text": s.text} for s in self.segments],
            "image_bboxes": [
                {"x": b.x, "y": b.y, "width": b.width, "height": b.height, "text": b.text, "confidence": b.confidence}
                for b in self.image_bboxes
            ],
            "audio_url": f"/media/{self.audio_output_path.split('/')[-1]}" if self.audio_output_path else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "error_message": self.error_message,
        }