import requests
from lib.logger import Logger
from config.DB_config import HEADERS_CONFIG

class MyRequests:
    @staticmethod
    def post(url: str, data: dict = None, files: dict = None):
        return MyRequests._send(url, data, 'POST', files)

    @staticmethod
    def get(url: str, data: dict = None):
        return MyRequests._send(url, data, 'GET')

    @staticmethod
    def put(url: str, data: dict = None):
        return MyRequests._send(url, data, 'PUT')

    @staticmethod
    def delete(url: str, data: dict = None):
        return MyRequests._send(url, data, 'DELETE')

    @staticmethod
    def _send(url: str, data: dict, method: str, files: dict = None):

        Logger.add_request(url, data, method)

        if method == 'GET':
            response = requests.get(url, json=data, headers=HEADERS_CONFIG)
        elif method == 'POST' and files is None:
            response = requests.post(url, json=data, headers=HEADERS_CONFIG)
        elif files is not None and method == 'POST':
            response = requests.post(url, json=data, headers=HEADERS_CONFIG, files=files)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=HEADERS_CONFIG)
        elif method == 'DELETE':
            response = requests.delete(url, json=data, headers=HEADERS_CONFIG)
        else:
            raise Exception(f"BAD HTTP METHOD '{method}'")

        Logger.add_response(response)

        return response
