import typing as t

from abc import ABC, abstractmethod
from auth_service.domain.contact import Contact
from auth_service.domain.sms_confirmation import SMSVerification
from auth_service.domain.user import User
from auth_service.domain.user_profile import UserProfile


class AuthDBManagerAbstract(ABC):
    @abstractmethod
    async def get_user_by_phone_number(self, phone_number: str) -> User:
        pass

    @abstractmethod
    async def get_user_by_user_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    async def save_user_state(self, user: User) -> t.Dict:
        pass

    @abstractmethod
    async def save_sms_confirmation(self, sms_confirmation: SMSVerification) -> None:
        pass

    @abstractmethod
    async def search_account_by_id_or_phone_number(self, user_id: str = None, phone_number: str = None) -> t.Dict:
        pass

    @abstractmethod
    async def get_all_my_contact(self, user_id):
        pass

    @abstractmethod
    async def get_my_account(self, user_id):
        pass

    @abstractmethod
    async def save_all_contacts(self, contact: Contact):
        pass

    @abstractmethod
    async def username_check(self, username: str):
        pass
