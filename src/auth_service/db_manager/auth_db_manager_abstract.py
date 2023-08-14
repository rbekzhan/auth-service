from abc import ABC, abstractmethod
import typing as t
from auth_service.domain.contact import Contact
from auth_service.domain.sms_confirmation import SMSConfirmation
from auth_service.domain.user_profile import UserProfile


class AuthDBManagerAbstract(ABC):
    @abstractmethod
    async def save_sms_confirmation(self, sms_confirmation: SMSConfirmation) -> None:
        pass

    @abstractmethod
    async def get_sms_confirmation(self, phone_number) -> SMSConfirmation:
        pass

    @abstractmethod
    async def update_sms_confirmation(self, sms_confirmation: SMSConfirmation) -> None:
        pass

    @abstractmethod
    async def create_account(self, user_profile: UserProfile) -> t.Dict:
        pass

    @abstractmethod
    async def contact_save(self, contact: Contact) -> None:
        pass

    @abstractmethod
    async def search_account(self, user_id, phone_number) -> t.Dict:
        pass