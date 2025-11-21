import asyncio
from .job_manager import JobManager
from .extractors import extract_text_from_media
from .translator import translate_text

class MediaProcessor:
    def __init__(self):
        self.job_manager = JobManager()

    async def process(self, job_id: str, file_path: str, target_language: str):
        try:
            self.job_manager.update_job(job_id, status="processing")

            # 1. Speech-to-text
            extracted_text = await extract_text_from_media(file_path)
            self.job_manager.update_job(job_id, extracted_text=extracted_text)

            # 2. Translation
            translated_text = await translate_text(extracted_text, target_language)

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
