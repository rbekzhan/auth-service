class CustomException(Exception):
    def __init__(self, message: str = None, status_code: int = None):
        self._message = message or self.__class__.__name__
        self._status_code = status_code or 404
        super().__init__(self._message, self._status_code)

    @property
    def message(self) -> str:
        return self._message

    @property
    def status_code(self) -> int:
        return self._status_code

    def __str__(self) -> str:
        return self.__class__.__name__


class NotFoundError(CustomException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
