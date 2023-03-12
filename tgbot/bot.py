from typing import Dict, Any, List, Tuple

import requests

from .objects import Update
from .stack import Stack
from .utils import Supabase
from .view import View


class Bot(Supabase):
    def __init__(
            self,
            tg_token: str,
            paths: Dict[str, View],
            supabase_endpoint: str,
            supabase_token: str,
            supabase_email: str,
            supabase_password: str,
            supabase_table: str,
            **kwargs
    ):
        Supabase.__init__(
            self,
            endpoint=supabase_endpoint,
            public_token=supabase_token,
            email=supabase_email,
            password=supabase_password
        )
        self._table = supabase_table
        self._tg_token = tg_token
        self._paths = paths

    def tg_token(self):
        return self._tg_token

    def _request(self, method: str, data: Dict[str, Any] = None):
        return requests.post(
            f"https://api.telegram.org/bot{self._tg_token}/{method}",
            json=data or {}
        ).json()

    def get_updates(self):
        return [Update(item) for item in self._request("getUpdates")]

    def send_message(self, text: str, keyboard: List[Tuple[str, str]]):
        self._request("sendMessage", data={
            "text": text
        })

    def _stack_get(self, user: int) -> List[str]:
        stacks = self.select(self._table, where={"user": user}, row_type=Stack)
        if len(stacks) == 1:
            return stacks[1].stack
        else:
            return ["/start"]

    def _stack_save(self, user: int, stack: List[str]):
        if len(self.select(self._table, where={"user": user})) == 0:
            self.insert(self._table, {"user": user, "stack": stack})
        else:
            self.update(self._table, {"user": user, "stack": stack}, {"user": user})

    def _view_get(self, path: str) -> View:
        return self._paths[path]

    def parse(self, update: Update):
        if all([
            update.message is not None,
            update.message.from_ is not None,
            update.message.from_.id == update.message.chat.id,
            update.message.text is not None
        ]):
            user = update.message.from_.id
            stack = self._stack_get(user)
            next_path = self._view_get(stack[-1]).on_text(update.message.text)
        elif update.callback_query is not None:
            user = update.callback_query.from_.id
            stack = self._stack_get(user)
            next_path = self._view_get(stack[-1]).on_callback(update.callback_query.id)
        else:
            return

        if next_path is None:
            return
        elif next_path == "__back__":
            stack.pop()
        else:
            stack.append(next_path)

        self._view_get(stack[-1]).run(self, update)
        self._stack_save(user, stack)
