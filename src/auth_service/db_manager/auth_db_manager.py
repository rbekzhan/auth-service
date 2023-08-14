import datetime
import logging
import uuid
import typing as t

from sqlalchemy.dialects.postgresql import insert as add
from auth_service.config import LOGGING_FORMAT
from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract
from auth_service.db_manager.db_manager import DBManagerBase
from auth_service.db_manager.tables import VerifyCode, UserTable, AccountTable, ContactTable
from auth_service.domain.contact import Contact
from auth_service.domain.sms_confirmation import SMSConfirmation
from sqlalchemy import insert, select, update, text, desc
from sqlalchemy.exc import IntegrityError

from auth_service.domain.user import User
from auth_service.domain.user_profile import UserProfile
from auth_service.schemas import UserProfileSchema, GetAccountWithContact, GetAccountInfoById

logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
log = logging.getLogger(__name__)


class DBManager(DBManagerBase, AuthDBManagerAbstract):
    async def save_sms_confirmation(self, sms_confirmation: SMSConfirmation):
        async with self.engine.begin() as connection:
            query = insert(VerifyCode)
            query = query.values(
                phone_number=sms_confirmation.phone_number,
                code=sms_confirmation.code_hash,
                attempt_count=sms_confirmation.attempt_count,
                confirm_code=sms_confirmation.confirm_code
            )
            await connection.execute(query)

    async def get_sms_confirmation(self, phone_number: str) -> (SMSConfirmation, None):
        async with self.engine.begin() as connection:
            query = select(VerifyCode)
            query = query.where(VerifyCode.c.phone_number == phone_number)
            query = query.order_by(desc(VerifyCode.c.created_at))
            cursor = await connection.execute(query)
            cursor = cursor.first()

            if not cursor:
                return

            query = select(UserTable)
            query = query.where(UserTable.c.phone_number == phone_number)
            user = await connection.execute(query)
            user = user.first()

            if user:
                user = User(phone_number=user.phone_number, user_id=str(user.id))
            else:
                user = None

            sms_confirmation = SMSConfirmation(
                sms_confirmation_id=str(cursor.id),
                user=user,
                code_hash=cursor.code,
                confirm_code=cursor.confirm_code,
                attempt_count=cursor.attempt_count,
                created_time=cursor.created_at
            )

            return sms_confirmation

    async def update_sms_confirmation(self, sms_confirmation: SMSConfirmation) -> None:
        async with self.engine.begin() as connection:
            query = update(VerifyCode)
            query = query.where(VerifyCode.c.id == sms_confirmation.sms_confirmation_id)
            query = query.values(
                confirm_code=sms_confirmation.confirm_code,
                code=sms_confirmation.code_hash,
                attempt_count=sms_confirmation.attempt_count,
                confirmed_client_code=sms_confirmation.confirmed_client_code
            )
            await connection.execute(query)

            if sms_confirmation.confirm_code:
                user = add(UserTable)
                user = user.values(id=sms_confirmation.user_id, phone_number=sms_confirmation.phone_number)
                user = user.on_conflict_do_nothing(index_elements=["phone_number"])
                await connection.execute(user)

    async def create_account(self, user_profile: UserProfile) -> t.Dict:
        async with self.engine.begin() as connection:
            try:
                account = insert(AccountTable)
                account = account.values(user_id=user_profile.user_id, username=user_profile.username,
                                         first_name=user_profile.first_name, last_name=user_profile.last_name,
                                         avatar_path=user_profile.avatar_path, bio=user_profile.bio)
                account = account.returning(AccountTable)
                cursor = await connection.execute(account)
                return UserProfileSchema().dump(cursor.first())
            except IntegrityError:
                return {"msg": "Пользователь с таким именем уже существует"}

    async def contact_save(self, contact: Contact) -> None:
        async with self.engine.begin() as connection:
            query = add(ContactTable)
            query = query.values(user_id=contact.user_id, phone_number=contact.phone_number,
                                 first_name=contact.first_name, last_name=contact.last_name)
            query = query.on_conflict_do_update(
                index_elements=["user_id", "phone_number"],
                set_=dict(first_name=contact.first_name, last_name=contact.last_name)
            )
            await connection.execute(query)

    async def search_account(self, user_id, phone_number) -> t.Dict:
        async with self.engine.begin() as connection:
            query = text(f""" with contact as (select first_name, last_name, phone_number, user_id
                                              from contacts
                                              where user_id = '{user_id}'
                                              )
                                              
                                    select contacts.*, accounts.username, accounts.avatar_path 
                                    from contacts
                                    join users on users.phone_number  = contacts.phone_number
                                    join accounts on accounts.user_id = users.id
                                    where users.phone_number = '{phone_number}'
                        """)
            cursor = await connection.execute(query)
            return GetAccountWithContact().dump(cursor.first())

    async def search_account_by_id_or_phone_number(self, user_id: str = None, phone_number: str = None) -> t.Dict:
        async with self.engine.begin() as connection:
            query = text(f"""select accounts.*
                             from users 
                             join accounts on users.id = accounts.user_id 
                             where (accounts.user_id = :user_id or users.phone_number = :phone_number)"""
                         )
            params = {'user_id': user_id,
                      'phone_number': phone_number}
            cursor = await connection.execute(query, params)
            return GetAccountInfoById().dump(cursor.first())

    async def get_all_my_contact(self, user_id):
        async with self.engine.begin() as connection:
            query = text(f""" with contact as (select first_name, last_name, phone_number, user_id
                                              from contacts
                                              where user_id = '{user_id}'
                                              )
                                              
                                    select contacts.*, accounts.username, accounts.avatar_path 
                                    from contacts
                                    join users on users.phone_number  = contacts.phone_number
                                    join accounts on accounts.user_id = users.id
                        """)
            cursor = await connection.execute(query)
            return GetAccountWithContact(many=True).dump(cursor)
