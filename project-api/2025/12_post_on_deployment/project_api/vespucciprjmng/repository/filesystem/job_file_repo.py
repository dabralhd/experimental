from datetime import datetime
from typing import List
from uuid import uuid4

from project_api.vespucciprjmng.dao.filesystem.file_dao_factory import (
    FileDAOFactory,
)
from project_api.vespucciprjmng.domain.job import Job, OperationType, State
from project_api.vespucciprjmng.repository.job_repo import JobRepo


class JobFileRepo(JobRepo):

    def __init__(self, tasks_folder_path: str):
        self.__dao_factory = FileDAOFactory(job_uri=tasks_folder_path)

    def get_jobs(self) -> List[Job]:
        return self.__dao_factory.get_job_dao_instance().get_all()

    def start_job(self, uuid: str, name: str, operation_type: OperationType, executer_id: str) -> Job:
        if not uuid:
            uuid = str(uuid4())
        new_task = Job(uuid=uuid, name=name, state=State.ON_GOING, start_time=datetime.now(), end_time=datetime.now(), operation_type=operation_type, executer_id=executer_id)
        self.__dao_factory.get_job_dao_instance().save(job=new_task)
        return new_task

    def stop_job(self, uuid: str, state_description: str = "", failure: bool = False) -> Job:
        task = self.__dao_factory.get_job_dao_instance().get(uuid=uuid)
        task.end_time = datetime.now()
        task.state_description = state_description
        task.state = State.TERMINATED_WITH_SUCCESS 
        if failure:
            task.state = State.TERMINATED_WITH_FAILURE
        
        self.__dao_factory.get_job_dao_instance().save(job=task)
        return task

    def remove_job(self, uuid: str) -> None:
        self.__dao_factory.get_job_dao_instance().delete(uuid=uuid)