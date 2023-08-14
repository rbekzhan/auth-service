import logging


class UsernameLengthCheck(Exception):
    def __init__(self, message):
        super().__init__(message)

    @property
    def username(self):
        return self._username


class EnglishLettersOnly(Exception):
    def __init__(self, message):
        super().__init__(message)


class UsernameFormatCheck(Exception):
    def __init__(self, message):
        super().__init__(message)


class PhoneNumberCheckDigits(Exception):
    def __init__(self, message):
        super().__init__(message)
