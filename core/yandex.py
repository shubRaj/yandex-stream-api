import requests
from bs4 import BeautifulSoup
import json


class Yandex:
    _BASE_DOWNLOAD_URL = "https://disk.yandex.com/public/api/download-url"
    _PROXIES = {
        "http": "http://smykbabu-rotate:kiy81fvox1h3@p.webshare.io:80",
        "https": "http://smykbabu-rotate:kiy81fvox1h3@p.webshare.io:80"
    }

    def __init__(self):
        self._session = requests.Session()
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "text/plain",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }

    def get_session(self):
        return self._session

    def close(self):
        self.get_session().close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback, exc_tb):
        self.close()

    def get_download(self, url):
        content = self.get_session().get(url).content
        soup = BeautifulSoup(content, "html.parser")
        json_data = soup.find("script", {"type": "application/json"}).text
        json_to_dict = json.loads(json_data)
        resource_id = json_to_dict.get("rootResourceId")
        resources = json_to_dict.get("resources")[resource_id]
        hash = resources["hash"]
        environment = json_to_dict.get("environment")
        sk = environment["sk"]
        data = json.dumps({
            "hash": hash,
            "sk": sk
        })
        session = self.get_session()
        session.headers.update({
            "Referer": url
        })
        return session.post(self._BASE_DOWNLOAD_URL, data=data, proxies=self._PROXIES).json()["data"]["url"]
