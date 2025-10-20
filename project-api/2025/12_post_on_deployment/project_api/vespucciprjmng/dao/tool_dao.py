
from __future__ import annotations

from abc import abstractmethod
from typing import Iterable

from project_api.vespucciprjmng.dao.dao import DAO
from project_api.vespucciprjmng.domain.tool import Tool


class ToolDAO(DAO):
    """Tool data access object"""

    @abstractmethod
    def get_all(self, project_id: str) -> Iterable[Tool]:
        pass
    
    @abstractmethod
    def get(self, project_id: str, model_id: str, tool_id: str) -> Tool:
        pass

    @abstractmethod
    def save(self, project_id: str, model_id: str, tool: Tool) -> None:
        pass

    @abstractmethod
    def delete(self, project_id: str, model_id: str, tool_id: str) -> None:
        pass