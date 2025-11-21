from dataclasses import dataclass, field
from enum import Enum
import uuid
from typing import Optional


class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

    @classmethod
    def _missing_(cls, value):
        """Делает enum нечувствительным к регистру и пробелам"""
        if not isinstance(value, str):
            return None
        value = value.strip().lower()
        for member in cls:
            if member.value == value:
                return member
        return cls.QUEUED


class FileType(str, Enum):
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"
    TEXT = "text"

    @classmethod
    def _missing_(cls, value):
        if not isinstance(value, str):
            return None
        value = value.strip().lower()
        for member in cls:
            if member.value == value:
                return member
        return None 


@dataclass
class Job:
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: JobStatus = JobStatus.QUEUED
    file_type: Optional[FileType] = None
    file_path: str = ""
    translated_text: str = ""
    audio_output_path: str = ""
    target_lang: str = ""
    error: str = ""
