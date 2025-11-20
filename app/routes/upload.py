"""
Upload route for handling media file uploads
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pathlib import Path
import logging
import asyncio
from app.models.job import Job, JobStatus, FileType
from app.services.job_manager import JobManager
from app.utils.file_utils import get_file_type, validate_file_size, save_uploaded_file
from app.config import UPLOAD_DIR, AUDIO_OUTPUT_DIR, MAX_FILE_SIZE
from app.routes.worker import process_media  # Добавлен импорт process_media

logger = logging.getLogger(__name__)

router = APIRouter()
job_manager = JobManager()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    target_lang: str = Form(...),
    background_tasks: BackgroundTasks = None
):
    """
    Upload media file and start translation job
    
    Args:
        file: Media file (audio, video, image, or text)
        target_lang: Target language (ru, en, kk)
        
    Returns:
        Job information with ID and status
    """
    try:
        # Validate target language
        if target_lang not in ["ru", "en", "kk"]:
            raise HTTPException(status_code=400, detail="Invalid target language")
        
        # Read file
        content = await file.read()
        
        # Validate file size
        if not validate_file_size(len(content), MAX_FILE_SIZE):
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE}MB"
            )
        
        # Determine file type
        mime_type = file.content_type or "application/octet-stream"
        file_type = get_file_type(mime_type)
        
        # Дополнительная валидация для TEXT (лимитируем текст, чтобы не перегружать mocks или реальные модели)
        if file_type == FileType.TEXT:
            text_content = content.decode('utf-8')
            if len(text_content) > 100000:  # Пример: лимит ~100k символов (~20-50 страниц текста)
                raise HTTPException(status_code=413, detail="Text file too large. Maximum characters: 100,000")
        
        # Create job
        job = job_manager.create_job(target_lang)
        job.file_type = file_type
        
        # Save uploaded file
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"{job.job_id}_{file.filename}"
        file_path = save_uploaded_file(UPLOAD_DIR, content, filename)
        job.file_path = file_path
        
        # Update job status
        job_manager.set_processing(job.job_id)
        
        # Add background task
        if background_tasks:
            background_tasks.add_task(
                process_media,
                job_id=job.job_id,
                file_path=file_path,
                file_type=file_type,
                target_lang=target_lang,
                job_manager=job_manager
            )
        else:
            # Fallback: process synchronously
            try:
                process_media(job.job_id, file_path, file_type, target_lang, job_manager)
            except Exception as e:
                logger.error(f"Error processing media: {e}")
                job_manager.set_failed(job.job_id, str(e))
        
        return {
            "job_id": job.job_id,
            "status": "processing",
            "message": "File uploaded successfully. Processing started."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")