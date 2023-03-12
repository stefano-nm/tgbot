from .chat import Chat
from .user import User
from ..utils import JSONObj


class Message(JSONObj):
    from_: User
    chat: Chat
    text: str
