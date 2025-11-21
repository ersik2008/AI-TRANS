import asyncio
import logging
from pathlib import Path
from app.models.job import FileType, JobStatus
from app.services.openai_client import translate_text
from app.services.speech_to_text import SpeechToTextService
from app.services.translation import TranslationService
from app.config import AUDIO_OUTPUT_DIR

logger = logging.getLogger(__name__)

# Глобальные экземпляры сервисов
speech_service = SpeechToTextService()
translation_service = TranslationService()

async def process_media(job_id: str, file_path: str, file_type: FileType, target_lang: str, job_manager):
    try:
        job_manager.set_processing(job_id)
        job = job_manager.get_job(job_id)
        
        # 1. Извлечение текста
        if file_type in [FileType.AUDIO, FileType.VIDEO]:
            transcript, _ = await speech_service.extract_text(file_path)
        elif file_type == FileType.IMAGE:
            transcript, _ = await speech_service.extract_text(file_path)  # Используем тот же сервис с OCR
        elif file_type == FileType.TEXT:
            with open(file_path, "r", encoding="utf-8") as f:
                transcript = f.read()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        # 2. Перевод
        translated_text = await translation_service.translate(transcript, target_lang)
        
        # 3. Сохранение результата
        AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = AUDIO_OUTPUT_DIR / f"{job_id}.txt"
        output_path.write_text(translated_text, encoding="utf-8")
        
        # 4. Обновление задания
        job_manager.update_job(
            job_id,
            translated_text=translated_text[:500] + "..." if len(translated_text) > 500 else translated_text,
            audio_output_path=str(output_path)
        )
        job_manager.set_completed(job_id)
        
        logger.info(f"Job {job_id} completed successfully")
        return translated_text
        
    except Exception as e:
        error_msg = f"Processing failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        job_manager.set_failed(job_id, error_msg)
        raise