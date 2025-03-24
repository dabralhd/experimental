
from __future__ import annotations

from abc import abstractmethod
from typing import Iterable

from project_api.vespucciprjmng.dao.dao import DAO
from project_api.vespucciprjmng.domain.log import Log


class LogDAO(DAO):
    """Log data access object"""

    @abstractmethod
    def get_all(self, project_id: str) -> Iterable[Log]:
        pass
    
    @abstractmethod
    def get(self, project_id: str, model_id: str = None, log_id: str = None) -> Log:
        pass

    @abstractmethod
    def update(self, project_id: str = None, model_id: str = None) -> None:
        pass
    
    @abstractmethod
    def save(self, project_id: str, model_id: str, log: Log) -> None:
        pass