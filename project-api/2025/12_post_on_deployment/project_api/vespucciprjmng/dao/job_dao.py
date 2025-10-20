
from __future__ import annotations

from abc import abstractmethod
from typing import List

from project_api.vespucciprjmng.dao.dao import DAO
from project_api.vespucciprjmng.domain.job import Job


class JobDAO(DAO):
    """Project data access object"""
    
    @abstractmethod
    def get_all() -> List[Job]:
        pass
    
    @abstractmethod
    def get(self, id: str) -> Job:
        pass

    @abstractmethod
    def save(self, task: Job) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass