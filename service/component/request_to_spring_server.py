import requests
import os
from dotenv import load_dotenv

load_dotenv()
from requests import RequestException

BASE_URL = os.getenv('SPRING_SERVER_URL')


class RequestToSpringServer:

    def __init__(self):
        pass

    @staticmethod
    def save_category(keyword: str, authorization_token: str) -> int:
        try:
            server_response = requests.post(BASE_URL + "/api/v1/categories", headers={
                'Authorization': authorization_token
            }, json={"name": keyword})
            print(f"Error: {server_response.status_code} - {server_response.text}")
            return server_response.json()['data']['categoryId']
        except RequestException:
            return -1
        except TypeError and KeyError:
            try:
                server_response = requests.get(BASE_URL + "/api/v1/categories/name/" + keyword, headers={
                    'Authorization': authorization_token
                })
                print(f"Error: {server_response.status_code} - {server_response.text}")
                return server_response.json()['data']['categoryId']
            except RequestException:
                return -1
