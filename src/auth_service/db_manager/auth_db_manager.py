import logging
import typing as t

from datetime import datetime
from auth_service.config import LOGGING_FORMAT, DB_SERVICE_URL
from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract
from auth_service.db_manager.db_tools import DBTools
from auth_service.domain.contact import Contact
from auth_service.domain.sms_confirmation import SMSConfirmation
from auth_service.domain.user import User
from auth_service.domain.user_profile import UserProfile
from auth_service.exception import NotFoundError

logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
log = logging.getLogger(__name__)


class DBManager(DBTools, AuthDBManagerAbstract):
    async def save_sms_confirmation(self, sms_confirmation: SMSConfirmation):
        result: t.Dict = await self.db_post(url=f"{DB_SERVICE_URL}/api/v1.0/send-sms",
                                            payload={
                                                "phone_number": sms_confirmation.phone_number,
                                                "code": sms_confirmation.code_hash,
                                                "attempt_count": sms_confirmation.attempt_count,
                                                "confirm_code": sms_confirmation.confirm_code
                                            }
                                            )

    async def get_sms_confirmation(self, phone_number: str) -> (SMSConfirmation, None):
        try:
            result: t.Dict = await self.db_get(url=f"{DB_SERVICE_URL}/api/v1.0/sms/{phone_number}")
        except NotFoundError:
            return

        if result["user_id"]:
            user = User(phone_number=result["phone_number"], user_id=str(result["user_id"]))
        else:
            user = None

        sms_confirmation = SMSConfirmation(
            sms_confirmation_id=str(result["sms_id"]),
            user=user,
            code_hash=result["code_hash"],
            confirm_code=result["confirm_code"],
            attempt_count=result["attempt_count"],
            created_time=datetime.strptime(result["created_time"], '%Y-%m-%d %H:%M:%S.%f')
        )

        return sms_confirmation

    async def update_sms_confirmation(self, sms_confirmation: SMSConfirmation) -> None:
        result: t.Dict = await self.db_post(url=f"{DB_SERVICE_URL}/api/v1.0/update-sms",
                                            payload={
                                                "phone_number": sms_confirmation.phone_number,
                                                "user_id": sms_confirmation.user_id,
                                                "sms_id": sms_confirmation.sms_confirmation_id,
                                                "code": sms_confirmation.code_hash,
                                                "attempt_count": sms_confirmation.attempt_count,
                                                "confirm_code": sms_confirmation.confirm_code,
                                                "confirmed_client_code": sms_confirmation.confirmed_client_code
                                            }
                                            )

    async def create_account(self, user_profile: UserProfile) -> t.Dict:
        result = await self.db_post(url=f"{DB_SERVICE_URL}/api/v1.0/accounts",
                                    payload={
                                        "user_id": str(user_profile.user_id),
                                        "username": user_profile.username,
                                        "name": user_profile.first_name,
                                        "surname": user_profile.last_name,
                                        "avatar_path": user_profile.avatar_path,
                                        "bio": user_profile.bio,
                                        "email": user_profile.email
                                    }
                                    )
        return result

    async def contact_save(self, contact: Contact) -> None:
        result = await self.db_post(url=f"{DB_SERVICE_URL}/api/v1.0/contacts",
                                    payload={
                                        "user_id": str(contact.user_id),
                                        "phone_number": contact.phone_number,
                                        "name": contact.last_name,
                                        "surname": contact.last_name
                                    }
                                    )

    async def search_contact_account(self, user_id, phone_number) -> t.Dict:
        result = await self.db_get(url=f"{DB_SERVICE_URL}/api/v1.0/contacts/{phone_number}/{user_id}")

        return result

    async def search_account_by_id_or_phone_number(self, user_id: str = None, phone_number: str = None) -> t.Dict:
        params = {
            "user_id": user_id,
            "phone_number": phone_number
        }
        result = await self.db_get(url=f"{DB_SERVICE_URL}/api/v1.0/accounts", params=params)

        return result

    async def get_all_my_contact(self, user_id):
        result = await self.db_get(url=f"{DB_SERVICE_URL}/api/v1.0/contacts/{user_id}")
        return result

    async def get_my_account(self, user_id):
        result = await self.db_get(url=f"{DB_SERVICE_URL}/api/v1.0/my-account/{user_id}")
        return result

    async def save_all_contacts(self, contact: Contact):
        pass
