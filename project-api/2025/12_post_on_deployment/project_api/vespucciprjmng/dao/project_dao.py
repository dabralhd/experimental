
from __future__ import annotations

from abc import abstractmethod
from typing import List

from project_api.vespucciprjmng.dao.dao import DAO
from project_api.vespucciprjmng.domain.project import Project


class ProjectDAO(DAO):
    """Project data access object"""
    
    @abstractmethod
    def get_all() -> List[Project]:
        pass
    
    @abstractmethod
    def get(self, id: str) -> Project:
        pass

    @abstractmethod
    def save(self, project: Project) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass

    @abstractmethod
    def update(self, project: Project) -> None:
        pass
