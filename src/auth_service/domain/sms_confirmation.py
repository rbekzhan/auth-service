from random import choice
from datetime import datetime, timedelta
from passlib.context import CryptContext
from auth_service.domain.user import User

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class SMSConfirmation:
    def __init__(self, sms_confirmation_id: str = None, user: User = None, message: str = None, code_hash: str = None,
                 created_time: datetime = None, confirm_code: bool = None, attempt_count: int = None,
                 confirmed_client_code: str = None):
        """
        :param phone: Номер телефона
        :param template: Текст смс
        :param reference: Ссылка на объект
        :param sent: Статус отправки
        :param code_hash: Хэш кода
        """

        self._sms_confirmation_id = sms_confirmation_id
        self._user = user
        self._message = message
        self._template = "Your code: {code}"
        self._code_hash = code_hash
        self._created_time = created_time
        self._attempt_count = attempt_count or 0
        self._confirm_code = confirm_code or False
        self._confirmed_client_code = confirmed_client_code
        self._life_time = 10

    @property
    def sms_confirmation_id(self) -> str:
        return self._sms_confirmation_id

    @property
    def phone_number(self) -> str:
        return self._user.phone_number

    @property
    def user_id(self) -> str:
        return str(self._user.user_id)

    @property
    def message(self) -> str:
        return self._message

    @property
    def template(self) -> str:
        return self._template

    @property
    def code_hash(self) -> str:
        return self._code_hash

    @property
    def created_time(self) -> datetime:
        return self._created_time

    @property
    def confirm_code(self) -> bool:
        return self._confirm_code

    @property
    def confirmed_client_code(self) -> str:
        return self._confirmed_client_code

    @property
    def attempt_count(self) -> int:
        return self._attempt_count

    def set_user(self, user: User) -> None:
        if not self._user:
            self._user = user

    @property
    def is_sms_lifetime_status(self) -> bool:
        """ Статус жизни СМС """
        now = datetime.timestamp(datetime.utcnow())
        created_date = datetime.timestamp(self._created_time + timedelta(minutes=self._life_time))
        return now < created_date

    @property
    def is_life_sms_confirmation(self) -> bool:
        """ Проверка на количество попыток и жизненного цикла смс """
        if not self._confirm_code and (self._attempt_count >= 5 or not self.is_sms_lifetime_status):
            return False
        return True

    def check(self):
        if self.is_life_sms_confirmation and self.is_sms_lifetime_status:
            raise ValueError("10 min block")

    def create_sms_message(self) -> None:
        """ Формирование СМС """
        code = "".join([choice("1234567890") for _ in range(6)])
        self._message = self._template.format(code=code)
        self._code_hash = pwd_context.hash(code)
        self._created_time = datetime.now()

    def confirm_sms_code(self, code) -> bool:
        """ Исключения проверки смс кода """
        if self._confirm_code:
            raise NotImplementedError("СМС код уже был активирован")
        if self._attempt_count >= 5:
            raise NotImplementedError("Слишком много попыток")
        if not self.is_sms_lifetime_status:
            raise NotImplementedError("СМС код устарел")
        self._attempt_count += 1
        if pwd_context.verify(code, self._code_hash):
            self._confirmed_client_code = code
            self._confirm_code = True
            return True
        return False
