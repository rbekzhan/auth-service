import re


class Contact:
    def __init__(self, user_id, first_name, last_name, phone_number):
        self._user_id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._phone_number = phone_number

    @property
    def user_id(self):
        return self._user_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def phone_number(self):
        return self._phone_number

    def is_valid_phone_number(self, phone_number):
        # Пример проверки для номера в формате "+1234567890"
        pattern = r'^\+[0-9]+$'
        if re.match(pattern, phone_number) is None:
            raise ValueError("Invalid phone number format")

