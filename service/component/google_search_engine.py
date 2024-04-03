import os
import requests

from dotenv import load_dotenv
from requests import RequestException


load_dotenv()

google_cse_api_key = os.getenv("GOOGLE_CSE_API_KEY")
google_search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")


class GoogleSearchEngineService:
    def __init__(self):
        pass

    @staticmethod
    def suggestion_of_the_day():
        url = f"https://www.googleapis.com/customsearch/v1?key={google_cse_api_key}&cx={google_search_engine_id}&q=쿼리"
        try:
            server_response = requests.get(url)
            print(server_response.json()['items'])
            return server_response.json()
        except RequestException as e:
            print(e)

    @staticmethod
    def suggestion_for_me(keywords: list[str]) -> dict:

        url = f"https://www.googleapis.com/customsearch/v1?key={google_cse_api_key}&cx={google_search_engine_id}&q={str(keywords)}"
        try:
            server_response = requests.get(url)
            print(server_response.json()['items'])
            return server_response.json()
        except RequestException as e:
            print(e)

