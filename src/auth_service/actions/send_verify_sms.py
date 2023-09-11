import typing
import jwt

from abc import ABC, abstractmethod
from datetime import timedelta, datetime
from auth_service.config import SECRET_KEY, redis_client
from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract as DBManager
from auth_service.domain.sms_confirmation import SMSVerification
from auth_service.domain.user import User
from auth_service.events import VerifyCodeEvent as Event
from auth_service.exception import ExpiredSignatureError, NotFoundError, NotCorrectCode


def generate_tokens(user_id):
    access_token = jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=20)
        },
        SECRET_KEY, algorithm="HS256"
    )

    refresh_token = jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(days=30)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    store_refresh_token_in_redis(user_id, refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}


def store_refresh_token_in_redis(user_id, refresh_token):
    refresh_key = f"refresh:{user_id}"
    redis_client.sadd(refresh_key, refresh_token)


class SendSmsInterface(ABC):
    @abstractmethod
    def send_sms(self, phone_number: str) -> typing.Dict:
        pass


class TOOAbilay(SendSmsInterface):
    def send_sms(self, phone_number: str) -> typing.Dict:
        return {"msg": "success"}


async def action_create_sms(phone_number: str, db_manager: DBManager):
    try:
        user: User = await db_manager.get_user_by_phone_number(phone_number=phone_number)
        last_sms_verification: SMSVerification = user.get_last_sms_verification()
        last_sms_verification.check()
    except NotFoundError:
        user = User(phone_number=phone_number)

    sms_verification = SMSVerification(phone_number=phone_number)
    sms_verification.create_sms_message()
    user.add_sms_verification(sms_verification=sms_verification)

    await db_manager.save_user_state(user=user)


async def action_verify_sms(event: Event, db_manager: DBManager):
    user: User = await db_manager.get_user_by_phone_number(phone_number=event.phone_number)
    sms_confirmation: SMSVerification = user.get_last_sms_verification()
    is_confirmed: bool = sms_confirmation.confirm_sms_code(code=event.code)
    await db_manager.save_user_state(user=user)

    if is_confirmed is False:
        raise NotCorrectCode(message="Неверный код подтверждения", code=2)

    tokens: typing.Dict = generate_tokens(user_id=user.user_id)

    if user.profile:
        return tokens | user.profile_to_dict()

    return tokens


async def action_refresh_token(token):
    try:
        decoded_refresh_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_refresh_token.get('user_id')
        refresh_key = f"refresh:{user_id}"
        stored_refresh_tokens = redis_client.smembers(refresh_key)
        provided_token_bytes = token.encode('utf-8')

        if provided_token_bytes in stored_refresh_tokens:
            redis_client.srem(refresh_key, provided_token_bytes)

            new_tokens = generate_tokens(user_id)

            return new_tokens
        else:
            raise Exception("Invalid refresh token")

    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError(message="Время действия токена истекло", code=4)


async def action_logout_token(token, user_id):
    decoded_access_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    refresh_key = f"refresh:{user_id}"
    stored_refresh_tokens = redis_client.smembers(refresh_key)
    token_encode = jwt.encode({"user_id": user_id, "exp": decoded_access_token.get('exp') + 2590800}, SECRET_KEY,
                              algorithm="HS256")
    provided_token_bytes = token_encode.encode('utf-8')
    if provided_token_bytes in stored_refresh_tokens:
        redis_client.srem(refresh_key, provided_token_bytes)
        redis_client.sadd("blacklist_access_tokens", token)
