import typing

from uuid import uuid4
from auth_service.domain.user_profile import UserProfile


class User:
    def __init__(self, phone_number: str, user_id: str = None, accounts: typing.List[UserProfile] = None):
        self._phone_number = phone_number
        self._user_id = user_id or uuid4()
        self._accounts = accounts

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def accounts(self) -> typing.List[UserProfile]:
        return self._accounts
