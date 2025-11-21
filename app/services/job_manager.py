from typing import Optional
import pkg_resources

class JobManager:
    def __init__(self):
        self.jobs = {}

    def create_job(self, target_lang: str) -> Job:
        job = Job(target_lang=target_lang)  # ✅ Теперь Job имеет target_lang
        self.jobs[job.job_id] = job
        return job

    def get_job(self, job_id: str) -> Optional[Job]:  # ✅ Изменено на Optional
        return self.jobs.get(job_id)

    def 

    def set_processing(self, job_id: str):
        if job := self.get_job(job_id):
            job.status = JobStatus.PROCESSING

    def set_completed(self, job_id: str):
        if job := self.get_job(job_id):
            job.status = JobStatus.COMPLETED

    def set_failed(self, job_id: str, error: str):
        if job := self.get_job(job_id):
            job.status = JobStatus.FAILED
            job.error = error