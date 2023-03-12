from .callback_query import CallbackQuery
from .message import Message
from ..utils import JSONObj


class Update(JSONObj):
    message: Message
    callback_query: CallbackQuery
