
from __future__ import annotations

from abc import abstractmethod
from typing import Iterable

from project_api.vespucciprjmng.dao.dao import DAO
from project_api.vespucciprjmng.domain.input import Input


class InputDAO(DAO):
    """Input data access object"""
    
    @abstractmethod
    def get_all(self, project_id: str) -> Iterable[Input]:
        pass
    
    @abstractmethod
    def get(self, project_id: str, model_id: str, input_id: str) -> Input:
        pass

    @abstractmethod
    def save(self, project_id: str, model_id: str, input: Input) -> None:
        pass

    @abstractmethod
    def delete(self, project_id: str, input_id: str) -> None:
        pass