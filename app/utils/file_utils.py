"""
File utilities for handling uploads and outputs
"""
import os
import mimetypes
from pathlib import Path
from app.models.job import FileType
import logging

logger = logging.getLogger(__name__)

def get_file_type(mime_type: str) -> FileType:
    """Determine file type from MIME type"""
    if mime_type.startswith("audio"):
        return FileType.AUDIO
    elif mime_type.startswith("video"):
        return FileType.VIDEO
    elif mime_type.startswith("image"):
        return FileType.IMAGE
    elif mime_type.startswith("text") or mime_type == "application/octet-stream":  # Добавлена поддержка text и octet-stream для .txt
        return FileType.TEXT
    else:
        raise ValueError(f"Unsupported file type: {mime_type}")

def validate_file_size(file_size: int, max_size_mb: int = 500) -> bool:
    """Validate file size"""
    max_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_bytes

def save_uploaded_file(upload_dir: Path, file_content: bytes, filename: str) -> str:
    """Save uploaded file and return path"""
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / filename
    with open(file_path, "wb") as f:
        f.write(file_content)
    logger.info(f"Saved file: {file_path}")
    return str(file_path)

def get_media_filename(job_id: str, extension: str) -> str:
    """Generate media filename"""
    return f"{job_id}.{extension}"