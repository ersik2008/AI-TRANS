import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/tmp/uploads"))
AUDIO_OUTPUT_DIR = Path(os.getenv("AUDIO_OUTPUT_DIR", "/tmp/audio_output"))

MAX_FILE_SIZE = 500  # MB

SUPPORTED_LANGUAGES = ["ru", "en", "kk"]
