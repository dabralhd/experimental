from __future__ import annotations

from enum import Enum
from typing import Any

from project_api.vespucciprjmng.domain.input import InputType
from project_api.vespucciprjmng.domain.model import ModelType
from project_api.vespucciprjmng.domain.output import OutputType


class ToolSection(Enum):
    INPUT   = "input"
    OUTPUT  = "output"
    
class ToolDescriptor():
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self.__name = name

    @property
    def uri(self) -> str:
        return self.__uri

    @uri.setter
    def uri(self, uri: str):
        if uri is None:
            raise ValueError("Invalid value for `uri`, must not be `None`")  # noqa: E501

        self.__uri = uri

    @property
    def parameters(self) -> Any:
        return self.__parameters

    @parameters.setter
    def parameters(self, parameters: Any):
        self.__parameters = parameters

    @property
    def runtime(self) -> str:
        return self.__runtime

    @runtime.setter
    def runtime(self, runtime: str):
        if runtime is None:
            raise ValueError("Invalid value for `runtime`, must not be `None`")  # noqa: E501

        self.__runtime = runtime

    def __init__(self, name: str, uri: str, runtime: str, version: str, parameters: Any, input_type: InputType, model_type: ModelType, output_type: OutputType, section: ToolSection) -> None:
        self.uri        = uri
        self.version    = version
        self.name       = name
        self.runtime    = runtime
        self.parameters = parameters
        self.input_type = input_type
        self.model_type = model_type
        self.output_type= output_type
        self.section    = section

    @staticmethod
    def deserialize(raw_tool: Any) -> ToolDescriptor:
        parameters = None
        if "tools_parameters" in raw_tool:
            parameters = raw_tool["tools_parameters"]
        return ToolDescriptor(name=raw_tool["name"], version=raw_tool["version"], input_type=InputType(raw_tool["input"]), model_type=ModelType(raw_tool["model"]), output_type=OutputType(raw_tool["output"]),  section=ToolSection(raw_tool["section"]), parameters=parameters, uri=raw_tool["uri"], runtime=raw_tool["runtime"])
