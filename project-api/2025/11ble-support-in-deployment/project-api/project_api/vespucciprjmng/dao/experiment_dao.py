
from __future__ import annotations

from abc import abstractmethod
from typing import Iterable

from project_api.vespucciprjmng.dao.dao import DAO
from project_api.vespucciprjmng.domain.experiment import Experiment


class ExperimentDAO(DAO):
    """Experiment data access object"""

    @abstractmethod
    def get_all(self, project_id: str, model_id: str = None) -> Iterable[Experiment]:
        pass
    
    @abstractmethod
    def get(self, project_name: str, model_id: str, experiment_id: str) -> Experiment:
        pass

    @abstractmethod
    def save(self, project_id: str, model_id: str, experiment: Experiment) -> None:
        pass

    @abstractmethod
    def delete(self, project_name: str, model_id: str, experiment_id: str) -> None:
        pass