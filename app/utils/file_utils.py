from pathlib import Path
from app.models.job import FileType

def get_file_type(mime_type: str) -> FileType:
    if mime_type.startswith("audio/"):
        return FileType.AUDIO
    elif mime_type.startswith("video/"):
        return FileType.VIDEO
    elif mime_type.startswith("image/"):
        return FileType.IMAGE
    elif mime_type in ["text/plain", "application/octet-stream"]:
        return FileType.TEXT
    else:
        return FileType.TEXT

def validate_file_size(size_bytes: int, max_mb: int) -> bool:
    return size_bytes <= max_mb * 1024 * 1024

def save_uploaded_file(directory: Path, content: bytes, filename: str) -> Path:
    file_path = directory / filename
    file_path.write_bytes(content)
    return file_path
