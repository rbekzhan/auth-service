import datetime

import jwt
import pytest

from auth_service.actions.send_verify_sms import action_create_sms, action_verify_sms
from auth_service.config import SECRET_KEY
from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract
from auth_service.domain.sms_confirmation import SMSConfirmation
from auth_service.domain.user import User
from auth_service.events import VerifyCodeEvent
from conftest import MockDBManager


class MockDBManager2(AuthDBManagerAbstract):
    async def get_sms_confirmation(self, phone_number):
        return SMSConfirmation(
            code_hash="$pbkdf2-sha256$29000$CEGIUSqFMMa411orhVDq3Q$U5qPGZiVeW8yQ9wp//lOUh4PWcJMdlGmKOYwsrFFTME",
            created_time=datetime.datetime.now(),
            attempt_count=0
        )

    async def save_sms_confirmation(self, sms_confirmation: SMSConfirmation):
        pass

    async def get_user_by_phone_number(self, phone_number):
        pass

    async def create_account(self, user_profile):
        pass


@pytest.mark.asyncio
async def test_create_sms():
    phone_number = "+77472095672"
    user = User(phone_number=phone_number)
    sms_confirmation = SMSConfirmation(user=user)
    sms_confirmation.create_sms_message()
    assert sms_confirmation.phone_number == phone_number
    assert sms_confirmation.template == "Your code: {code}"
    assert isinstance(sms_confirmation.created_time, datetime.datetime)
    message = sms_confirmation.message
    code = "".join([i for i in message if i.isdigit()])
    assert len(code) == 4


@pytest.mark.asyncio
async def test_action_create_sms():
    phone_number = "+77472095672"
    result = await action_create_sms(phone_number=phone_number, db_manager=MockDBManager())
    assert isinstance(result, str)
    code = "".join([i for i in result if i.isdigit()])
    template = "".join([i for i in result if not i.isdigit()])
    assert len(code) == 4
    assert code.isdigit()
    assert template == "Your code: "
    assert template + code == f"Your code: {code}"


@pytest.mark.asyncio
async def test_action_verify_sms(mock_dbmanager=MockDBManager()):
    number = "+77472095672"
    event = VerifyCodeEvent(phone_number=number, code='9292')
    token = await action_verify_sms(event=event, db_manager=mock_dbmanager)
    assert jwt.decode(token.get("access_token"), SECRET_KEY, algorithms=["HS256"]) == {'user_id': 'f797d67d-a90b-4ea6-a3c9-29e17a14e487'}

# TODO: без юзера проверить токен
