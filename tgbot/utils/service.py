from threading import Thread
from typing import Callable, ParamSpec

import requests
from requests import Response

_P = ParamSpec("_P")


def to_thread(method: Callable[_P, Response]):
    def decorator(*args: _P.args, **kwargs: _P.kwargs):
        def _thread():
            status = -1
            while status != 200:
                response = method(*args, **kwargs)
                status = response.status_code

        Thread(target=_thread, daemon=True).start()

    return decorator


class Service:
    def __init__(
            self,
            name: str,
            address: str,
            catalog: str,
            token: str = None
    ):
        self._service_name = name
        self._service_catalog = catalog
        self._service_address = address
        self._service_token = token
        self.service_register()

    @to_thread
    def service_register(self):
        return requests.post(f"{self._service_catalog}/register", params={
            "name": self._service_name,
            "endpoint": self._service_address,
            "token": self._service_token
        })

    @to_thread
    def service_unregister(self):
        return requests.delete(f"{self._service_catalog}/unregister", params={
            "name": self._service_name,
            "token": self._service_token
        })
