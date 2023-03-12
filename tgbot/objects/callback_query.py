from .user import User
from ..utils import JSONObj


class CallbackQuery(JSONObj):
    id: str
    from_: User
