import asyncio
from pathlib import Path
import subprocess
from openai import OpenAI
from faster_whisper import WhisperModel
import pytesseract
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "whisper-1")

client = OpenAI(api_key=OPENAI_API_KEY)

# faster-whisper модель (быстрее и локальная)
faster_model = WhisperModel("medium", device="cpu", compute_type="int8")

# Если tesseract не стоит — установить:
# sudo apt install tesseract-ocr
# pip install pytesseract
# pip install pillow


async def extract_text_from_media(file_path: str) -> str:
    file_path = Path(file_path)
    ext = file_path.suffix.lower()

    try:
        if ext in [".mp3", ".wav", ".m4a", ".flac"]:
            return await extract_from_audio(file_path)
        elif ext in [".mp4", ".avi", ".mov", ".mkv"]:
            return await extract_from_video(file_path)
        elif ext in [".jpg", ".jpeg", ".png", ".gif"]:
            return await extract_from_image(file_path)
        else:
            return "Unsupported file format."
    except Exception as e:
        return f"Error extracting text: {e}"


async def extract_from_audio(file_path: Path) -> str:
    """
    Текст из аудио:
    - сначала пробуем faster-whisper (быстрее)
    - затем можно переключить на OpenAI whisper-1
    """

    print("➡ Using Faster-Whisper...")

    segments, info = faster_model.transcribe(str(file_path), beam_size=5)
    text = " ".join([seg.text for seg in segments])

    if text.strip():
        return text

    print("➡ Using OpenAI Whisper (fallback)...")

    with open(file_path, "rb") as f:
        response = client.audio.transcriptions.create(
            model=OPENAI_MODEL,
            file=f
        )
    return response.text



async def extract_from_video(file_path: Path) -> str:
    """
    Видео → аудио → текст
    """
    audio_path = file_path.with_suffix(".wav")

    # Выделяем аудио из видео
    cmd = ["ffmpeg", "-y", "-i", str(file_path), "-vn", "-acodec", "pcm_s16le", str(audio_path)]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return await extract_from_audio(audio_path)


async def extract_from_image(file_path: Path) -> str:
    """
    OCR через tesseract
    """
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img, lang="eng+rus")
    return text.strip()


if __name__ == "__main__":
    async def main():
        result = await extract_text_from_media("example.mp4")
        print(result)

    asyncio.run(main())
