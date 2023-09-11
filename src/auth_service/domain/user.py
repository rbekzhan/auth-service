import typing as t

from uuid import uuid4
from auth_service.domain.contact import Contact
from auth_service.domain.sms_confirmation import SMSVerification
from auth_service.domain.user_profile import UserProfile


class User:
    _cursor_contact: Contact

    def __init__(
            self,
            user_id: str = None,
            phone_number: str = None,
            contacts: t.List[Contact] = None,
            sms_verifications: t.List[SMSVerification] = None,
            profile: UserProfile = None
    ):
        self._user_id = user_id or uuid4()
        self._phone_number = phone_number
        self._contacts = contacts or []
        self._sms_verifications = sms_verifications or []
        self._profile = profile

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def profile(self) -> UserProfile:
        return self._profile

    @property
    def sms_verifications(self) -> t.List[SMSVerification]:
        return self._sms_verifications

    @property
    def contacts(self) -> t.List[Contact]:
        return self._contacts

    def add_sms_verification(self, sms_verification: SMSVerification) -> None:
        self._sms_verifications.append(sms_verification)

    def add_contact(self, contact: Contact) -> None:
        self._contacts.append(contact)

    def get_last_sms_verification(self) -> SMSVerification:
        if len(self._sms_verifications) > 0:
            return self._sms_verifications[-1]

    @property
    def cursor_contact(self) -> Contact:
        return self._cursor_contact

    def set_cursor_contact(self, contact: Contact) -> None:
        for cont in self._contacts:
            if cont.phone_number == contact.phone_number:
                self._cursor_contact = cont

    def profile_to_dict(self) -> t.Dict:
        return {
            "user": {
                "user_id": self._profile.user_id,
                "username": self._profile.username,
                "name": self._profile.name,
                "surname": self._profile.surname,
                "email": self._profile.email,
                "avatar_path": self._profile.avatar_path,
                "bio": self._profile.bio
            }
        }

    def set_profile(self, profile: UserProfile) -> None:
        if self._profile is None:
            self._profile = profile
