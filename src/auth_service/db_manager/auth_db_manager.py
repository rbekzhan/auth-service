import logging
import typing as t

from datetime import datetime
from auth_service.config import LOGGING_FORMAT, DB_SERVICE_URL
from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract
from auth_service.db_manager.db_tools import DBTools
from auth_service.domain.contact import Contact
from auth_service.domain.sms_confirmation import SMSVerification
from auth_service.domain.user import User
from auth_service.domain.user_profile import UserProfile
from auth_service.exception import NotFoundError

logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
log = logging.getLogger(__name__)


class DBManager(DBTools, AuthDBManagerAbstract):
    async def save_sms_confirmation(self, sms_confirmation: SMSVerification):
        await self.db_post(url=f"{DB_SERVICE_URL}/api/v1.0/send-sms",
                           payload={
                               "phone_number": sms_confirmation.phone_number,
                               "code": "$pbkdf2-sha256$29000$BqD0/p9Tyvmfk5LSWut9zw$FuZP4F4Z6QmWicuyVDtPUyUSSRoFOcBa/diSj3jy5uw",
                               "attempt_count": sms_confirmation.attempt_count,
                               "confirm_code": sms_confirmation.confirm_code
                           }
                           )

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

    async def username_check(self, username: str) -> t.Dict:
        params = {
            "username": username
        }
        return await self.db_get(url=f"{DB_SERVICE_URL}/api/v1.0/accounts/username-check", params=params)

    async def _create_user_object(self, data: t.Dict) -> User:
        contacts_list: t.List = []
        for contact in data['contacts']:
            contact_profile = None
            if contact["contact_profile"] is not None:
                cont = contact["contact_profile"]
                contact_profile = UserProfile(
                    user_profile_id=cont["user_profile_id"],
                    user_id=cont["user_id"],
                    username=cont["username"],
                    name=cont["name"],
                    surname=cont["surname"],
                    email=cont["email"],
                    avatar_path=cont["avatar_path"],
                    bio=cont["bio"],
                )

            contact = Contact(
                contact_id=contact["contact_id"],
                user_id=contact["user_id"],
                phone_number=contact["phone_number"],
                name=contact["name"],
                surname=contact["surname"],
                contact_profile=contact_profile
            )
            contacts_list.append(contact)

        sms_verifications_list: t.List = []
        for sms_verification in data['sms_verifications']:
            sms_confirmation = SMSVerification(
                sms_verification_id=sms_verification["verify_code_id"],
                phone_number=sms_verification["phone_number"],
                code_hash=sms_verification["code_hash"],
                confirm_code=sms_verification["confirm_code"],
                attempt_count=sms_verification["attempt_count"],
                created_at=datetime.strptime(sms_verification["created_at"], '%Y-%m-%d %H:%M:%S.%f'),
                updated_at=datetime.strptime(
                    sms_verification["updated_at"], '%Y-%m-%d %H:%M:%S.%f'
                ) if sms_verification["updated_at"] is not None else None
            )
            sms_verifications_list.append(sms_confirmation)

        user_profile = data["profile"]
        if user_profile is not None:
            user_profile = UserProfile(
                user_profile_id=user_profile["user_profile_id"],
                user_id=user_profile["user_id"],
                username=user_profile["username"],
                name=user_profile["name"],
                surname=user_profile["surname"],
                email=user_profile["email"],
                avatar_path=user_profile["avatar_path"],
                bio=user_profile["bio"]
            )

        user = User(
            user_id=data["user_id"],
            phone_number=data["phone_number"],
            contacts=contacts_list,
            sms_verifications=sms_verifications_list,
            profile=user_profile
        )

        return user

    async def get_user_by_phone_number(self, phone_number) -> User:
        data: t.Dict = await self.db_get(url=f"{DB_SERVICE_URL}/api/v1.0/users/phone_number/{phone_number}")
        return await self._create_user_object(data=data)

    async def get_user_by_user_id(self, user_id: str) -> User:
        data: t.Dict = await self.db_get(url=f"{DB_SERVICE_URL}/api/v1.0/users/id/{user_id}")
        return await self._create_user_object(data=data)

    async def save_user_state(self, user: User) -> t.Dict:
        contacts_list: t.List[t.Dict] = []
        for contact in user.contacts:
            contact_dict = {
                "contact_id": str(contact.contact_id),
                "user_id": str(contact.user_id),
                "phone_number": contact.phone_number,
                "name": contact.name,
                "surname": contact.surname,
            }
            contacts_list.append(contact_dict)

        sms_verifications_list: t.List[t.Dict] = []
        for sms_verification in user.sms_verifications:
            sms_verification = {
                "sms_verification_id": str(sms_verification.sms_verification_id),
                "phone_number": sms_verification.phone_number,
                "code_hash": sms_verification.code_hash,
                "confirmed_client_code": sms_verification.confirmed_client_code,
                "confirm_code": sms_verification.confirm_code,
                "attempt_count": sms_verification.attempt_count,
                "created_at": str(sms_verification.created_at),
                "updated_at": str(sms_verification.updated_at) if sms_verification.updated_at is not None else None,
            }
            sms_verifications_list.append(sms_verification)

        user_profile_dict = None
        if user.profile:
            user_profile_dict = {
                "user_profile_id": str(user.profile.user_profile_id),
                "user_id": str(user.profile.user_id),
                "username": user.profile.username,
                "name": user.profile.name,
                "surname": user.profile.surname,
                "email": user.profile.email,
                "avatar_path": user.profile.avatar_path,
                "bio": user.profile.bio,
            }

        user_dict = {
            "user_id": str(user.user_id),
            "phone_number": user.phone_number,
            "profile": user_profile_dict,
            "contacts": contacts_list,
            "sms_verifications": sms_verifications_list
        }

        await self.db_post(
            url=f"{DB_SERVICE_URL}/api/v1.0/users",
            payload=user_dict
        )
        return user_dict
