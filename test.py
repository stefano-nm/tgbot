from config import config
from tgbot import Bot

tgbot = Bot(**config)

while True:
    for update in tgbot.get_updates():
        tgbot.parse(update)
