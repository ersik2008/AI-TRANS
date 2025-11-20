import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

class JobManager:
    """Manages job state and persistence"""
    
    def __init__(self):
        self.jobs_dir = Path("jobs")
        self.jobs_dir.mkdir(exist_ok=True)
        self.jobs = {}
        self._load_jobs()

    def create_job(self, job_id: str, file_path: str, target_language: str, original_filename: str):
        """Create a new job"""
        job = {
            "job_id": job_id,
            "file_path": file_path,
            "target_language": target_language,
            "original_filename": original_filename,
            "status": "queued",
            "extracted_text": "",
            "translated_text": "",
            "error": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.jobs[job_id] = job
        self._save_job(job_id, job)
        return job

    def update_job(self, job_id: str, **updates):
        """Update job status and results"""
        if job_id not in self.jobs:
            return None
        
        self.jobs[job_id].update(updates)
        self.jobs[job_id]["updated_at"] = datetime.now().isoformat()
        self._save_job(job_id, self.jobs[job_id])
        return self.jobs[job_id]

    def get_job(self, job_id: str) -> Optional[Dict]:
        """Get job details"""
        return self.jobs.get(job_id)

    def list_jobs(self) -> List[Dict]:
        """List all jobs"""
        return list(self.jobs.values())

    def delete_job(self, job_id: str):
        """Delete a job"""
        if job_id in self.jobs:
            del self.jobs[job_id]
            job_file = self.jobs_dir / f"{job_id}.json"
            if job_file.exists():
                job_file.unlink()

    def _save_job(self, job_id: str, job: Dict):
        """Persist job to disk"""
        job_file = self.jobs_dir / f"{job_id}.json"
        with open(job_file, "w") as f:
            json.dump(job, f)

    def _load_jobs(self):
        """Load jobs from disk"""
        for job_file in self.jobs_dir.glob("*.json"):
            with open(job_file) as f:
                job = json.load(f)
                self.jobs[job["job_id"]] = job
