from typing import List

from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ
from project_api.vespucciprjmng.domain.model import Model
from project_api.vespucciprjmng.domain.test import Test
from project_api.vespucciprjmng.domain.tool import Tool


class OutputType(str):
    pass

class Output(DomainOBJ):
    """Output data model"""

    @property
    def uuid(self) -> str:
        return self.__uuid

    @uuid.setter 
    def uuid(self, value: str):
        self.__uuid = value

    @property
    def output_type(self) -> OutputType:
        return self.__output_type

    @output_type.setter 
    def output_type(self, value: OutputType):
        self.__output_type = value

    @property
    def model_ref(self) -> Model:
        return self.__model_ref

    @model_ref.setter 
    def model_ref(self, value: Model):
        self.__model_ref = value

    @property
    def tests(self) -> List[Test]:
        return self.__tests

    @tests.setter 
    def tests(self, value: List[Test]):
        self.__tests = value

    @property
    def best_test(self) -> Test:
        return self.__best_test

    @best_test.setter 
    def best_test(self, value: Test):
        self.__best_test = value

    @property
    def tools(self) -> List[Tool]:
        return self.__tools

    @tools.setter 
    def tools(self, value: List[Tool]):
        self.__tools = value


    def __init__(self, uuid: str = None, model_ref: Model = None, output_type: OutputType = None, tests: List[Test] = None, best_test: Test = None, tools: List[Tool] = []):
        self.__uuid         = uuid
        self.__model_ref    = model_ref
        self.__output_type  = output_type
        self.__tests        = tests
        self.__best_test    = best_test
        self.__tools        = tools