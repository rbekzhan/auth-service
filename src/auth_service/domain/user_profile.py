import re
import uuid

from auth_service.exception import UsernameLengthCheck, EnglishLettersOnly, UsernameFormatCheck


class UserProfile:
    def __init__(
            self,
            user_profile_id: uuid = None,
            user_id: uuid = None,
            username: str = None,
            name: str = None,
            surname: str = None,
            avatar_path: str = None,
            bio: str = None,
            email: str = None
    ):
        self._user_profile_id = user_profile_id or uuid.uuid4()
        self._user_id = user_id
        self._username = username
        self._first_name = name
        self._last_name = surname
        self._avatar_path = avatar_path
        self._bio = bio
        self._email = email

    @property
    def user_profile_id(self) -> str:
        return str(self._user_profile_id)

    @property
    def user_id(self) -> str:
        return str(self._user_id)

    @property
    def username(self) -> str:
        """ Ссылка для активации """
        return self._username

    @property
    def name(self) -> str:
        return self._first_name

    @property
    def surname(self) -> str:
        return self._last_name

    @property
    def avatar_path(self) -> str:
        return self._avatar_path

    @property
    def bio(self) -> str:
        return self._bio

    @property
    def email(self) -> str:
        return self._email

    def is_valid_username(self):
        # Проверка на длину имени пользователя
        if len(self._username) < 6 or len(self._username) > 15:
            raise UsernameLengthCheck(message="Мало символа")

        # Проверка на наличие только английских букв и цифр в имени пользователя
        if not re.match("^[a-zA-Z0-9._-]+$", self._username):
            raise EnglishLettersOnly(message="username должна состоит из английских букв")

        # Проверка, чтобы первый символ не был цифрой
        if self._username[0].isdigit():
            raise UsernameFormatCheck(message="первый символ не может быть цифрой")
