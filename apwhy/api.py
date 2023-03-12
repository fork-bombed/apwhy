from urllib.parse import urlparse
import requests


class Api:
    def __init__(self, url: str) -> None:
        self._parsed_url = urlparse(url)
        self.domain = self._parsed_url.hostname
        self.protocol = self._parsed_url.scheme
        self.port = self._parsed_url.port
        self.path = self._trim_path(self._parsed_url.path)

    def _trim_path(self, path: str) -> str:
        if len(path) >= 1:
            if path[-1] == "/":
                return path[:-1]
        return path

    def get_url(self) -> str:
        url_builder = []
        url_builder.append(f"{self.protocol}://")
        url_builder.append(self.domain)
        if self.port is not None:
            url_builder.append(f":{self.port}")
        url_builder.append(f"{self.path}")
        return "".join(url_builder)

    def get_url_from_path(self, path: str) -> str:
        return f"{self.get_url()}/{self._trim_path(path)}"


class Endpoint:
    def __init__(self, api: Api, path: str) -> None:
        self.path = path
        self.url = api.get_url_from_path(path)
        self.responses = []

    def get_path(self) -> str:
        return self.path

    def get_url(self) -> str:
        return self.url

    def get_responses(self) -> list[requests.Response]:
        return self.responses

    def probe(self) -> requests.Response:
        return self._get()

    def method_sweep(self) -> None:
        self._post()
        self._put()
        self._delete()
        self._head()
        self._patch()

    def _get(self) -> requests.Response:
        response = requests.get(url=self.url)
        self.responses.append(response)
        return response

    def _post(self) -> requests.Response:
        response = requests.post(url=self.url)
        self.responses.append(response)
        return response

    def _put(self) -> requests.Response:
        response = requests.put(url=self.url)
        self.responses.append(response)
        return response

    def _delete(self) -> requests.Response:
        response = requests.delete(url=self.url)
        self.responses.append(response)
        return response

    def _head(self) -> requests.Response:
        response = requests.head(url=self.url)
        self.responses.append(response)
        return response

    def _patch(self) -> requests.Response:
        response = requests.patch(url=self.url)
        self.responses.append(response)
        return response
