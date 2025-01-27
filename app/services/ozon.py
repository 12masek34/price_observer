import re

from aiogram import (
    types,
)


class OzonSubsciberService:

    def __init__(self, message: types.Message) -> None:
        self.message = message
        self.url = self.get_url()

    def get_url(self) -> str:
        if not self.message.text:
            return ""

        url_pattern = re.compile(r"https?://[^\s]+")
        match = url_pattern.search(self.message.text)
        return match.group(0) if match else ""

    def subscribe(self):
        import pdb; pdb.set_trace();
        return "foo"
