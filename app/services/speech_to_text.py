import asyncio
from faster_whisper import WhisperModel
import subprocess
from pathlib import Path

class SpeechToTextService:
    def __init__(self):
        self.model = WhisperModel("base", device="cpu", compute_type="int8")
    
    async def extract_text(self, file_path: str) -> tuple[str, list]:
        loop = asyncio.get_running_loop()
        
        # Для видео сначала извлекаем аудио
        if file_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            audio_path = await self._extract_audio(file_path)
            file_path = str(audio_path)
        
        # Асинхронный вызов транскрипции
        segments, _ = await loop.run_in_executor(
            None, 
            lambda: self.model.transcribe(file_path, beam_size=5)
        )
        
        full_text = " ".join([seg.text for seg in segments])
        return full_text, segments
    
    async def _extract_audio(self, video_path: str) -> Path:
        audio_path = Path(video_path).with_suffix('.wav')
        cmd = [
            'ffmpeg', '-y', '-i', video_path,
            '-vn', '-acodec', 'pcm_s16le', 
            '-ar', '16000', str(audio_path)
        ]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        await process.wait()
        return audio_path