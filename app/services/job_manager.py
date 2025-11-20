"""
Job manager for tracking and managing translation jobs
"""
from app.models.job import Job, JobStatus
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)

class JobManager:
    """Manages all translation jobs"""
    
    def __init__(self):
        self.jobs: Dict[str, Job] = {}
    
    def create_job(self, target_lang: str) -> Job:
        """Create a new job"""
        job = Job(target_lang=target_lang)
        self.jobs[job.job_id] = job
        logger.info(f"Created job {job.job_id}")
        return job
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Retrieve a job by ID"""
        return self.jobs.get(job_id)
    
    def update_job(self, job_id: str, **kwargs) -> Optional[Job]:
        """Update job attributes"""
        job = self.jobs.get(job_id)
        if job:
            for key, value in kwargs.items():
                if hasattr(job, key):
                    setattr(job, key, value)
            job.updated_at = __import__('datetime').datetime.now().isoformat()
            logger.info(f"Updated job {job_id}: {kwargs}")
        return job
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all jobs as dictionaries"""
        return [job.to_dict() for job in self.jobs.values()]
    
    def set_processing(self, job_id: str):
        """Mark job as processing"""
        self.update_job(job_id, status=JobStatus.PROCESSING)
    
    def set_completed(self, job_id: str):
        """Mark job as completed"""
        self.update_job(job_id, status=JobStatus.COMPLETED)
    
    def set_failed(self, job_id: str, error: str):
        """Mark job as failed with error message"""
        self.update_job(job_id, status=JobStatus.FAILED, error_message=error)
