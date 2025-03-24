
from __future__ import annotations

from abc import abstractmethod
from typing import Iterable

from project_api.vespucciprjmng.dao.dao import DAO
from project_api.vespucciprjmng.domain.deployment import Deployment


class DeploymentDAO(DAO):
    """Deployment data access object"""

    @abstractmethod
    def get_all(self, project_id: str) -> Iterable[Deployment]:
        pass
    
    @abstractmethod
    def get(self, project_id: str, deployment_id: str) -> Deployment:
        pass

    @abstractmethod
    def update(self, project_id: str, deployment_id: str) -> None:
        pass
    
    @abstractmethod
    def save(self, project_id: str, output: Deployment) -> None:
        pass