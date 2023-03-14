from urllib.parse import urlparse
import aiohttp


def trim_path_end(path: str) -> str:
    if path.endswith("/"):
        return path[:-1]
    return path


def trim_path_start(path: str) -> str:
    if path.startswith("/"):
        return path[1:]
    return path


def trim_path(path: str) -> str:
    path = trim_path_start(path)
    path = trim_path_end(path)
    return path


class Api:
    def __init__(self, url: str) -> None:
        self._parsed_url = urlparse(url)
        self.domain = self._parsed_url.hostname
        self.protocol = self._parsed_url.scheme
        self.port = self._parsed_url.port
        self.path = trim_path_end(self._parsed_url.path)

    def get_url(self) -> str:
        url_builder = []
        url_builder.append(f"{self.protocol}://")
        url_builder.append(self.domain)
        if self.port is not None:
            url_builder.append(f":{self.port}")
        url_builder.append(f"{self.path}")
        return "".join(url_builder)

    def get_url_from_path(self, path: str) -> str:
        return f"{self.get_url()}/{trim_path(path)}"


class Endpoint:
    def __init__(self, api: Api, session: aiohttp.ClientSession, path: str) -> None:
        self.path = trim_path(path)
        self.url = api.get_url_from_path(self.path)
        self.session = session

    def get_path(self) -> str:
        return self.path

    def get_url(self) -> str:
        return self.url

    async def get(self):
        return await self.session.get(url=self.url)

    async def post(self, data=None):
        return await self.session.post(url=self.url, data=data)
    
    async def put(self, data=None):
        return await self.session.put(url=self.url, data=data)
    
    async def patch(self, data=None):
        return await self.session.patch(url=self.url, data=data)
    
    async def head(self):
        return await self.session.head(url=self.url)

    async def delete(self):
        return await self.session.delete(url=self.url)
