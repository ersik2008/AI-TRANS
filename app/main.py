"""
AI-Translate Backend API
FastAPI server for handling media translation workflows
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
import logging
from pathlib import Path
from app.routes import upload, results
from app.services.job_manager import JobManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create necessary directories
UPLOAD_DIR = Path("/tmp/uploads")
AUDIO_OUTPUT_DIR = Path("/tmp/audio_output")
UPLOAD_DIR.mkdir(exist_ok=True)
AUDIO_OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize job manager
job_manager = JobManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    logger.info("AI-Translate Backend started")
    yield
    logger.info("AI-Translate Backend shutdown")

app = FastAPI(
    title="AI-Translate API",
    description="Media translation service with multilingual support",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(results.router, prefix="/api", tags=["results"])

# Serve static files
if AUDIO_OUTPUT_DIR.exists():
    app.mount("/media", StaticFiles(directory=AUDIO_OUTPUT_DIR), name="media")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI-Translate",
        "version": "1.0.0"
    }

@app.get("/api/jobs")
async def list_jobs():
    """List all jobs"""
    return {
        "jobs": job_manager.get_all_jobs(),
        "total": len(job_manager.jobs)
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
