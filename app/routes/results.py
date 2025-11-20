"""
Results route for retrieving translation results
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import logging
from app.routes.upload import job_manager

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/result/{job_id}")
async def get_result(job_id: str):
    """
    Retrieve translation results for a job
    
    Args:
        job_id: Job ID
        
    Returns:
        Job result with translated text and metadata
    """
    job = job_manager.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job.to_dict()

@router.get("/audio/{job_id}")
async def download_audio(job_id: str):
    """
    Download generated audio file
    
    Args:
        job_id: Job ID
        
    Returns:
        Audio file
    """
    job = job_manager.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if not job.audio_output_path or not Path(job.audio_output_path).exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        job.audio_output_path,
        media_type="audio/mpeg",
        filename=f"{job_id}.mp3"
    )
