
from urllib.parse import urljoin

import requests

from project_api.vespucciprjmng.dao.data_session import DataSession


class HTTPDataConnector(DataSession):
    def __init__(self, uri: str):
        super().__init__(uri)
        
    def get(self, subpath):
        url = urljoin(self._uri, subpath)
        response = requests.get(url)
        self.__check_response(response)
        json_response = response.json()
        return json_response

    def put(self, subpath, body):
        url = urljoin(self._uri, subpath)
        res = requests.put(url, json=body, headers={"Content-Type":"application/json"})
        self.__check_response(res)
        return

    def post(self, subpath, body):
        url = urljoin(self._uri, subpath)
        res = requests.post(url, json=body, headers={"Content-Type":"application/json"})
        self.__check_response(res)
        return

    def delete(self, subpath: str):
        url = urljoin(self._uri, subpath)
        res = requests.delete(url)
        self.__check_response(res)
        return

    def dispose(self):
        pass

    def __check_response(self, response: requests.Response):
        if response.status_code >=200 and response.status_code < 300:
            return response
        raise Exception(response.text)