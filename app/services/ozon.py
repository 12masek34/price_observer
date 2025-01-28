import re

from aiogram import (
    types,
)
from app.services.base import BaseSubscriberService


class OzonSubsciberService(BaseSubscriberService):

    def __init__(self, message: types.Message) -> None:
        super().__init__(message)


    def subscribe(self):
        import pdb; pdb.set_trace();
        return "foo"
