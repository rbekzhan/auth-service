import pytest

from auth_service.domain.user import User


def test_init_user():
    phone_number = '+77472095672'
    user = User(phone_number=phone_number)
    assert user.phone_number == phone_number
