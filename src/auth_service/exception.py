class CustomBaseException(Exception):
    def __init__(self, status_code: int, message: str = None):
        self._status_code = status_code
        self._message = message or self.__class__.__name__
        super().__init__(self._message, self._status_code)

    @property
    def message(self) -> str:
        return self._message

    @property
    def status_code(self) -> int:
        return self._status_code

    def __str__(self) -> str:
        return self.__class__.__name__


class SMSCodeExpired(CustomBaseException):
    def __init__(self, status_code: int = None, message: str = None):
        self._status_code = status_code or 403
        self._message = message or self.__class__.__name__
        super().__init__(self._status_code, self._message)


class SMSCodeWasActivated(CustomBaseException):
    def __init__(self, status_code: int = None, message: str = None):
        self._status_code = status_code or 400
        self._message = message or self.__class__.__name__
        super().__init__(self._status_code, self._message)


class TooManyTries(CustomBaseException):
    def __init__(self, status_code: int = None, message: str = None):
        self._status_code = status_code or 429
        self._message = message or self.__class__.__name__
        super().__init__(self._status_code, self._message)


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


class EnglishLettersOnly(Exception):
    def __init__(self, message):
        super().__init__(message)


class UsernameFormatCheck(Exception):
    def __init__(self, message):
        super().__init__(message)


class PhoneNumberCheckDigits(Exception):
    def __init__(self, message):
        super().__init__(message)
