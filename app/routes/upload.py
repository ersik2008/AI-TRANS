from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from pathlib import Path
import logging
from app.models.job import FileType
from app.services.job_manager import JobManager
from app.utils.file_utils import get_file_type, validate_file_size, save_uploaded_file
from app.config import UPLOAD_DIR, MAX_FILE_SIZE
from app.routes.worker import process_media

logger = logging.getLogger(__name__)
router = APIRouter()
job_manager = JobManager()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    target_lang: str = Form(...),
    background_tasks: BackgroundTasks = None
):
    try:
        if target_lang not in ["ru", "en", "kk"]:
            raise HTTPException(status_code=400, detail="Invalid target language")
        
        content = await file.read()
        if not validate_file_size(len(content), MAX_FILE_SIZE):
            raise HTTPException(status_code=413, detail="File too large")
        
        mime_type = file.content_type or "application/octet-stream"
        file_type = get_file_type(mime_type)

        if file_type == FileType.TEXT:
            text_content = content.decode("utf-8")
            if len(text_content) > 100000:
                raise HTTPException(status_code=413, detail="Text file too large")
        
        job = job_manager.create_job(target_lang)
        job.file_type = file_type

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"{job.job_id}_{file.filename}"
        file_path = save_uploaded_file(UPLOAD_DIR, content, filename)
        job.file_path = file_path

        if background_tasks:
            background_tasks.add_task(process_media, job.job_id, file_path, file_type, target_lang, job_manager)
        else:
            process_media(job.job_id, file_path, file_type, target_lang, job_manager)

        return {"job_id": job.job_id, "status": "processing", "message": "File uploaded successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")
