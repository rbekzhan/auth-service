from datetime import datetime
import typing as t
from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract
from auth_service.domain.contact import Contact
from auth_service.domain.sms_confirmation import SMSConfirmation
from auth_service.domain.user import User


class MockDBManager(AuthDBManagerAbstract):
    async def get_sms_confirmation(self, phone_number):
        user = User(phone_number=phone_number, user_id='f797d67d-a90b-4ea6-a3c9-29e17a14e487')
        return SMSConfirmation(
            user=user,
            code_hash="$pbkdf2-sha256$29000$CEGIUSqFMMa411orhVDq3Q$U5qPGZiVeW8yQ9wp//lOUh4PWcJMdlGmKOYwsrFFTME",
            created_time=datetime.now(),
            attempt_count=0
        )

    async def save_sms_confirmation(self, sms_confirmation: SMSConfirmation):
        pass

    async def get_user_by_phone_number(self, phone_number):
        pass

    async def update_sms_confirmation(self, sms_confirmation: SMSConfirmation) -> None:
        pass

    async def create_account(self, user_profile):
        return {
                "last_name": "Rakhmetzhan",
                "user_id": "7f4b2f8a-145a-458f-bc4a-08c041b89b71",
                "bio": "tester",
                "first_name": "Bekzhan",
                "username": "rbekzhan"
                }

    async def contact_save(self, contact: Contact) -> None:
        pass

    async def search_contact_account(self, user_id, phone_number) -> t.Dict:
        return {
                "last_name": "Rakhmetzhan",
                "user_id": "664e623b-a85c-4a41-84d5-d666b34f530c",
                "first_name": "Bek",
                "username": "bekzhanf",
            }
