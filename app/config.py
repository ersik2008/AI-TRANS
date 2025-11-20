"""
Configuration and constants
"""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/tmp/uploads"))
AUDIO_OUTPUT_DIR = Path(os.getenv("AUDIO_OUTPUT_DIR", "/tmp/audio_output"))

# Model paths
MODELS_DIR = Path(os.getenv("MODELS_DIR", "/tmp/models"))

# Supported languages
SUPPORTED_LANGUAGES = {
    "ru": "Russian",
    "kk": "Kazakh",
    "en": "English",
}

# Supported NLLB language codes
NLLB_LANG_CODES = {
    "ru": "rus_Cyrl",
    "en": "eng_Latn",
    "kk": "kaz_Cyrl",
}

# File size limits (in MB)
MAX_FILE_SIZE = 500  # 500 MB

# Processing timeouts (in seconds)
WHISPER_TIMEOUT = 3600
OCR_TIMEOUT = 600
TRANSLATION_TIMEOUT = 600
TTS_TIMEOUT = 600

# Model settings
WHISPER_MODEL = "base"  # "tiny", "base", "small", "medium", "large"
NLLB_MODEL = "facebook/nllb-200-distilled-600M"
TTS_MODEL = "tts_models/en/ljspeech/glow-tts"  # Will be overridden based on language
