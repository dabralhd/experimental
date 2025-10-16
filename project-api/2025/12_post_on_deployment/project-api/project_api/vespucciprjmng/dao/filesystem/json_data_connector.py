
import json
import shutil
from os import listdir, makedirs, path
from typing import Any

from project_api.vespucciprjmng.dao.data_session import DataSession


class JSONDataConnector(DataSession):

    @property
    def json_file(self) -> Any:
        return self.__json_file

    def __init__(self, uri: str):
        super().__init__(uri)
        self.__uri      = uri
        self.__json_file= None

    def list_files(self):
        return listdir(self.__uri)

    def init(self, filename: str):
        file_path = path.join(self.__uri, filename)
        makedirs(path.dirname(file_path), exist_ok=True)
        fp = open(file_path, "w")
        fp.write("{}")
        fp.close()
        
    def connect(self, filename: str):
        self.__uri_file = path.join(self.__uri, filename)
        with open(self.__uri_file) as json_file:
            self.__json_file = json.load(json_file)

    def save(self):
        with open(self.__uri_file, "w") as json_file:
            json_file.write(json.dumps(self.__json_file, indent=4))

    def delete(self, filename = None):
        if not filename:
            shutil.rmtree(path.dirname(path.join(self.__uri_file)))      
        else:
            shutil.rmtree(path.dirname(path.join(self.__uri, filename)))    

    def dispose(self):
        self.__json_file = None
        self.__uri_file = None