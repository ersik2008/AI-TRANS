from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import uuid
import asyncio
from pathlib import Path
import json
from datetime import datetime

from services.job_manager import JobManager
from services.media_processor import MediaProcessor

app = FastAPI(
    title="AI-Translate API",
    description="Media recognition and translation API",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
job_manager = JobManager()
media_processor = MediaProcessor()

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    target_language: str = Form(...)
):
    """Upload media file for processing"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_path = UPLOAD_DIR / job_id / file.filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        # Create job
        job_manager.create_job(
            job_id=job_id,
            file_path=str(file_path),
            target_language=target_language,
            original_filename=file.filename
        )

        # Start processing in background
        asyncio.create_task(
            media_processor.process(job_id, str(file_path), target_language)
        )

        return {
            "job_id": job_id,
            "status": "processing",
            "message": "File uploaded successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/result/{job_id}")
async def get_result(job_id: str):
    """Get processing result for a job"""
    try:
        job = job_manager.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/jobs")
async def list_jobs():
    """List all jobs"""
    return job_manager.list_jobs()

@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a job"""
    try:
        job_manager.delete_job(job_id)
        return {"message": "Job deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
