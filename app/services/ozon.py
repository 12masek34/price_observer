from aiogram import (
    types,
)


class OzonSubsciberService:

    def __init__(self, message: types.Message) -> None:
        self.message = message

    def subscribe(self):
        return "foo"
