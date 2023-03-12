from typing import List

from tgbot.utils import JSONObj


class Stack(JSONObj):
    user: int
    stack: List[str]
