import requests
import os
from dotenv import load_dotenv

load_dotenv()
from requests import RequestException

URL = os.getenv('SPRING_SERVER_URL')


class RequestToSpringServer:

    def __init__(self):
        pass

    @staticmethod
    def save_category(keyword: str) -> int:
        try:
            server_response = requests.post(URL, json={"name": keyword})
            return server_response.json()['data']['categoryId']
        except RequestException:
            return -1
