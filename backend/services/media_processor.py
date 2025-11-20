import asyncio
from pathlib import Path
from .job_manager import JobManager
from .extractors import extract_text_from_media
from .translator import translate_text

class MediaProcessor:
    """Processes media files and manages translation workflow"""
    
    def __init__(self):
        self.job_manager = JobManager()

    async def process(self, job_id: str, file_path: str, target_language: str):
        """Process media file: extract text and translate"""
        try:
            self.job_manager.update_job(job_id, status="processing")

            # Extract text from media
            extracted_text = await extract_text_from_media(file_path)
            self.job_manager.update_job(job_id, extracted_text=extracted_text)

            # Translate text
            translated_text = await translate_text(extracted_text, target_language)

            # Update job with results
            self.job_manager.update_job(
                job_id,
                status="completed",
                translated_text=translated_text
            )

        except Exception as e:
            self.job_manager.update_job(
                job_id,
                status="failed",
                error=str(e)
            )
