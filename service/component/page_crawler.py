import requests
from bs4 import BeautifulSoup


class PageCrawler:
    def __init__(self):
        pass

    @staticmethod
    def get_page_contents(url: str) -> str:
        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            body_text = ''.join(p.get_text(strip=True) for p in soup.find_all('p'))
            if body_text == "":
                raise Exception
            return body_text
        else:
            print(response.status_code)
