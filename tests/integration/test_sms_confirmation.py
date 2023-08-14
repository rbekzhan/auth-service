from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from auth_service.config import DB_DSN
from auth_service.db_manager.auth_db_manager import DBManager
from auth_service.db_manager.tables import metadata
from auth_service.domain.sms_confirmation import SMSConfirmation
from auth_service.domain.user import User


@pytest.mark.asyncio
async def test_create_sms():
    metadata.drop_all(bind=create_async_engine(DB_DSN, echo=True, future=True))
    metadata.create_all()
    db_manager = DBManager()
    phone_number = "+77472095521"
    user = User(phone_number=phone_number)
    sms_confirmation = SMSConfirmation(user=user)
    sms_confirmation.create_sms_message()
    await db_manager.save_sms_confirmation(sms_confirmation=sms_confirmation)
    # verify_code =
    # assert sms_confirmation.phone_number == verify_code.phone_number
