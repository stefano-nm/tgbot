from threading import Lock
from typing import ParamSpec, Dict, Any, List, TypeVar, Type, overload

import requests

from .jsonobj import JSONObj

_P = ParamSpec("_P")
_T = TypeVar("_T", bound=JSONObj)


class Supabase:
    def __init__(self, endpoint: str, public_token: str, email: str, password: str):
        self._endpoint = endpoint
        self._public_token = public_token
        self._access_token = ""
        self._email = email
        self._password = password
        self._lock = Lock()
        self._signup()

    def _request(self, *args, **kwargs):
        with self._lock:
            response = requests.request(*args, **kwargs)
            if response.status_code == 401:
                self._login()
                response = requests.request(*args, **kwargs)
            if response.text:
                return response.json()

    def _signup(self):
        return self._request(
            "POST",
            f"{self._endpoint}/auth/v1/signup",
            headers={
                "apikey": self._public_token,
                "Content-Type": "application/json"
            },
            json={
                "email": self._email,
                "password": self._password
            }
        )

    def _login(self):
        response = self._request(
            "POST"
            f"{self._endpoint}/auth/v1/token?grant_type=password",
            headers={
                "apikey": self._public_token,
                "Content-Type": "application/json"
            },
            json={
                "email": self._email,
                "password": self._password
            }
        )
        self._access_token = response["access_token"]

    @overload
    def select(
            self,
            table: str,
            *,
            cols: List[str] = None,
            where: Dict[str, Any] = None,
    ) -> List[Dict[str, str]]:
        ...

    @overload
    def select(
            self,
            table: str,
            *,
            cols: List[str] = None,
            where: Dict[str, Any] = None,
            row_type: Type[_T] = None,
    ) -> List[_T]:
        ...

    def select(
            self,
            table: str,
            *,
            cols: List[str] = None,
            where: Dict[str, Any] = None,
            row_type: Type[_T] = None
    ):
        cols = cols or ["*"]
        where = where or {}
        response = self._request(
            "GET",
            f"{self._endpoint}/rest/v1/{table}?" + "&".join(
                [f"{col}=eq.{val}" for col, val in where.items()] + ["select=" + ",".join(cols)]),
            headers={
                "apikey": self._public_token,
                "Authorization": f"Bearer {self._access_token}"
            }
        )
        if row_type is None:
            return response
        else:
            return [row_type(item) for item in response]

    def insert(
            self,
            table: str,
            cols: Dict[str, Any]
    ):
        self._request(
            "POST",
            f"{self._endpoint}/rest/v1/{table}",
            headers={
                "apikey": self._public_token,
                "Authorization": f"Bearer {self._access_token}",
                "Content-Type": "application/json"
            },
            json=cols
        )

    def update(
            self,
            table: str,
            values: Dict[str, Any],
            where: Dict[str, Any]
    ):
        self._request(
            "PATCH",
            f"{self._endpoint}/rest/v1/{table}?" + "&".join([
                f"{col}=eq.{value}" for col, value in where.items()
            ]),
            headers={
                "apikey": self._public_token,
                "Authorization": f"Bearer {self._access_token}",
                "Content-Type": "application/json"
            },
            json=values
        )

    def delete(
            self,
            table: str,
            where: Dict[str, Any]
    ):
        self._request(
            "DELETE",
            f"{self._endpoint}/rest/v1/{table}?" + "&".join([
                f"{col}=eq.{value}" for col, value in where.items()
            ]),
            headers={
                "apikey": self._public_token,
                "Authorization": f"Bearer {self._access_token}"
            }
        )
