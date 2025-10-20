
from abc import abstractmethod


class DataSession():

    def __init__(self, uri: str):
        self._uri = uri

    @abstractmethod
    def save():
        pass

    @abstractmethod
    def dispose():
        pass