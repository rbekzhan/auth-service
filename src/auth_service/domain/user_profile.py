import re

from auth_service.exception import UsernameLengthCheck, EnglishLettersOnly, UsernameFormatCheck


class UserProfile:
    def __init__(self,
                 user_id: str,
                 username: str,
                 first_name: str = None,
                 last_name: str = None,
                 bio: str = None):
        self._user_id = user_id
        self._username = username
        self._first_name = first_name
        self._last_name = last_name
        self._bio = bio

    @property
    def user_id(self):
        return self._user_id

    @property
    def username(self) -> str:
        """ Ссылка для активации """
        return self._username

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def bio(self) -> str:
        return self._bio

    def is_valid_username(self):
        # Проверка на длину имени пользователя
        if len(self._username) < 6 or len(self._username) > 15:
            raise UsernameLengthCheck(message="Мало символа")

        # Проверка на наличие только английских букв и цифр в имени пользователя
        if not re.match("^[a-zA-Z0-9]+$", self._username):
            raise EnglishLettersOnly(message="username должна состоит из английских букв")

        # Проверка, чтобы первый символ не был цифрой
        if self._username[0].isdigit():
            raise UsernameFormatCheck(message="первый символ не может быть цифрой")
