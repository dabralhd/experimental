
from __future__ import annotations

from abc import abstractmethod
from typing import Iterable

from project_api.vespucciprjmng.dao.dao import DAO
from project_api.vespucciprjmng.domain.output import Output


class OutputDAO(DAO):
    """Output data access object"""

    @abstractmethod
    def get_all(self, project_id: str) -> Iterable[Output]:
        pass
    
    @abstractmethod
    def get(self, project_id: str, model_id: str, output_id: str) -> Output:
        pass

    @abstractmethod
    def update(self, project_id: str, model_id: str) -> None:
        pass
    
    @abstractmethod
    def save(self, project_id: str, model_id: str, output: Output) -> None:
        pass