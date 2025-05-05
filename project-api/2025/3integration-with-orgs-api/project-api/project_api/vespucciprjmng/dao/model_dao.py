
from __future__ import annotations

from abc import abstractmethod
from typing import List

from project_api.vespucciprjmng.dao.dao import DAO
from project_api.vespucciprjmng.domain.model import Model
from project_api.vespucciprjmng.domain.project import Project


class ModelDAO(DAO):
    """Model data access object"""
    
    @abstractmethod
    def get_all(self, project_id: str = None) -> List[Model]:
        pass

    @abstractmethod
    def get(self, model_id: str, project_id: str = None) -> Model:
        pass

    @abstractmethod
    def save(self, model: Model) -> None:
        pass

    @abstractmethod
    def delete(self, project_id: str, model_id: str) -> None:
        pass

    @abstractmethod
    def update(self, project: Project) -> None:
        pass