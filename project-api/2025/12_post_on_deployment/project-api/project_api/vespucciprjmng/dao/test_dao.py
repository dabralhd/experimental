
from __future__ import annotations

from abc import abstractmethod
from typing import Iterable

from project_api.vespucciprjmng.dao.dao import DAO
from project_api.vespucciprjmng.domain.test import Test


class TestDAO(DAO):
    """Test data access object"""

    @abstractmethod
    def get_all(self, project_id: str) -> Iterable[Test]:
        pass
    
    @abstractmethod
    def get(self, project_id: str, model_id: str = None, test_id: str = None) -> Test:
        pass

    @abstractmethod
    def update(self, project_id: str = None, model_id: str = None) -> None:
        pass
    
    @abstractmethod
    def save(self, project_id: str, model_id: str, test: Test) -> None:
        pass