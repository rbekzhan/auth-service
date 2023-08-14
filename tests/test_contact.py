import pytest

from auth_service.actions.contact import action_contact_save
from auth_service.domain.contact import Contact
from auth_service.events import ContactEvent
from conftest import MockDBManager


@pytest.mark.asyncio
async def test_contact():
    contact = Contact(user_id="664e623b-a85c-4a41-84d5-d666b34f530c",
                      phone_number="+77712790202",
                      first_name="Bek",
                      last_name="Rakhmetzhan")

    assert contact.user_id == "664e623b-a85c-4a41-84d5-d666b34f530c"
    assert contact.phone_number == "+77712790202"
    assert contact.first_name == "Bek"
    assert contact.last_name != "Rakмhmetzhan"


@pytest.mark.asyncio
async def test_is_valid_phone_number():
    contact = Contact(
        user_id="664e623b-a85c-4a41-84d5-d666b34f530c",
        phone_number="+77712790202",
        first_name="Bek",
        last_name="Rakhmetzhan"
    )

    valid_phone_number = "+77712790202"
    invalid_phone_number = "12345"

    assert contact.is_valid_phone_number(valid_phone_number) is None

    with pytest.raises(ValueError, match="Invalid phone number format"):
        contact.is_valid_phone_number(invalid_phone_number)


@pytest.mark.asyncio
async def test_action_contact_save(db_manager=MockDBManager()):
    event = ContactEvent(
        user_id="664e623b-a85c-4a41-84d5-d666b34f530c",
        phone_number="+77712790202",
        first_name="Bek",
        last_name="Rakhmetzhan"
    )
    result = await action_contact_save(event=event, db_manager=db_manager)
    assert result == {
                "last_name": "Rakhmetzhan",
                "user_id": "664e623b-a85c-4a41-84d5-d666b34f530c",
                "first_name": "Bek",
                "username": "bekzhanf",
            }

    assert result != {
                "last_name": "Raxkhmetzhan",
                "user_id": "664e623b-a85c-4a41-84d5-d666b34f530c",
                "first_name": "Bek",
                "username": "bekzhanf",
                }

