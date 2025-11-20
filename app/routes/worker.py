"""
Background worker for processing media files
"""
import logging
from pathlib import Path
from app.models.job import FileType
from app.services.speech_to_text import SpeechToTextService, MockSpeechToTextService
from app.services.image_to_text import ImageToTextService, MockImageToTextService
from app.services.translation import TranslationService, MockTranslationService
from app.services.text_to_speech import TextToSpeechService, MockTextToSpeechService
from app.config import AUDIO_OUTPUT_DIR

logger = logging.getLogger(__name__)

def process_media(job_id: str, file_path: str, file_type: FileType, target_lang: str, job_manager):
    """
    Process media file: extract text, translate, and generate speech
    """
    try:
        logger.info(f"Processing job {job_id}: file_type={file_type}, lang={target_lang}")
        
        source_text = ""
        segments = []
        bboxes = []
        
        # Initialize services (using mock for demo)
        if file_type in [FileType.AUDIO, FileType.VIDEO]:
            stt_service = MockSpeechToTextService()
            source_text, segments = stt_service.extract_text(file_path)
        elif file_type == FileType.IMAGE:
            ocr_service = MockImageToTextService()
            source_text, bboxes = ocr_service.extract_text(file_path)
        elif file_type == FileType.TEXT:  # Новая ветка для текста
            with open(file_path, 'r', encoding='utf-8') as f:
                source_text = f.read().strip()
            # segments и bboxes остаются пустыми
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Update source text and results
        job_manager.update_job(job_id, source_text=source_text, segments=segments, image_bboxes=bboxes)
        
        # Translate
        translation_service = MockTranslationService()
        translated_text = translation_service.translate(source_text, target_lang)
        job_manager.update_job(job_id, translated_text=translated_text)
        
        # Generate speech
        AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        audio_output = AUDIO_OUTPUT_DIR / f"{job_id}.mp3"
        
        tts_service = MockTextToSpeechService()
        success = tts_service.generate_speech(
            translated_text,
            str(audio_output),
            lang=target_lang
        )
        
        if success:
            job_manager.update_job(job_id, audio_output_path=str(audio_output))
        
        # Mark as completed
        job_manager.set_completed(job_id)
        logger.info(f"Job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Error processing job {job_id}: {e}")
        job_manager.set_failed(job_id, str(e))