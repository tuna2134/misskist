from aiohttp import ClientSession

from asyncio import AbstractEventLoop
from typing import Optional


class HttpException(Exception):
    pass


class Route:

    def __init__(self, method: str, path: str):
        self.method = method
        self.path = path

    def __str__(self):
        return f"{self.method} {self.path}"


class NotFound(HttpException):

    def __init__(self, route: Route):
        super().__init__(f"Route {route} not found")


class RestAPI:

    def __init__(self, endpoint: str, loop: Optional[AbstractEventLoop] = None, ssl: bool = False):
        self.endpoint = endpoint
        self._session = ClientSession(loop=loop)
        self.ssl = ssl

    async def request(self, route: Route, **kwargs):
        if self.ssl:
            url = "https://" + self.endpoint
        else:
            url = "http://" + self.endpoint
        res = await self._session.request(route.method, url, **kwargs)
        if res.status == 204:
            return None
        elif res.status == 200:
            if res.headers.get("Content-Type") == "application/json":
                return await res.json()
            else:
                return res
        elif res.status == 404:
            raise NotFound(route)


    def ws_connect(self, token: str):
        if self.ssl:
            url = "wss://" + self.endpoint
        else:
            url = "ws://" + self.endpoint
        return self._session.ws_connect(url + "/streaming?i=" + token)