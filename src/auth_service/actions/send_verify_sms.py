import typing
import jwt

from abc import ABC, abstractmethod
from auth_service.config import SECRET_KEY
from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract as DBManager
from auth_service.domain.sms_confirmation import SMSConfirmation
from auth_service.domain.user import User


class SendSmsInterface(ABC):
    @abstractmethod
    def send_sms(self, phone_number: str) -> typing.Dict:
        pass


class TOOAbilay(SendSmsInterface):
    def send_sms(self, phone_number: str) -> typing.Dict:
        return {"msg": "success"}


async def action_create_sms(phone_number: str, db_manager: DBManager):
    sms_confirmation: SMSConfirmation = await db_manager.get_sms_confirmation(phone_number=phone_number)
    if sms_confirmation:
        sms_confirmation.check()

    user = User(phone_number=phone_number)
    sms_confirmation = SMSConfirmation(user=user)
    sms_confirmation.create_sms_message()
    await db_manager.save_sms_confirmation(sms_confirmation=sms_confirmation)

    sms_company = TOOAbilay()
    result = sms_company.send_sms(phone_number=phone_number)
    return result


async def action_verify_sms(event, db_manager: DBManager):
    sms_confirmation: SMSConfirmation = await db_manager.get_sms_confirmation(phone_number=event.phone_number)
    sms_confirmation.confirm_sms_code(code=event.code)

    if sms_confirmation.confirm_code:
        user = User(phone_number=event.phone_number)
        sms_confirmation.set_user(user=user)

    await db_manager.update_sms_confirmation(sms_confirmation=sms_confirmation)
    my_user_profile = await db_manager.get_my_account(user_id=sms_confirmation.user_id)

    if sms_confirmation.confirm_code:
        return {"access_token": jwt.encode({"user_id": sms_confirmation.user_id}, SECRET_KEY, algorithm="HS256"),
                "my_user_profile": my_user_profile
                }

    return {"msg": "code is not correct"}
