from typing import Optional

from .objects import Update


class View:
    def on_text(
            self,
            text: str
    ) -> Optional[str]:
        return None

    def on_callback(
            self,
            callback: str
    ) -> Optional[str]:
        return None

    def run(self, bot, update: Update):
        pass
