from typing import List

from project_api.vespucciprjmng.domain.job import Job


class JobRepo():
    
    def get_jobs(self) -> List[Job]:
        pass

    def create_job(self, *args) -> Job:
        pass
    
    def remove_job(self, *args) -> None:
        pass