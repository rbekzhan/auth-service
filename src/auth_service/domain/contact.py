import re
from uuid import uuid4, UUID

from auth_service.domain.user_profile import UserProfile


class Contact:
    def __init__(
            self,
            contact_id: UUID = None,
            user_id: UUID = None,
            phone_number: str = None,
            name: str = None,
            surname: str = None,
            contact_profile: UserProfile = None
    ):
        self._contact_id = contact_id or uuid4()
        self._user_id = user_id
        self._phone_number = phone_number
        self._name = name
        self._surname = surname
        self._contact_profile = contact_profile

    @property
    def contact_id(self):
        return self._contact_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def name(self):
        return self._name

    @property
    def surname(self):
        return self._surname

    @property
    def phone_number(self):
        return self._phone_number

    @property
    def contact_profile(self):
        return self._contact_profile

    def is_valid_phone_number(self, phone_number):
        # Пример проверки для номера в формате "+1234567890"
        pattern = r'^\+[0-9]+$'
        if re.match(pattern, phone_number) is None:
            raise ValueError("Invalid phone number format")
