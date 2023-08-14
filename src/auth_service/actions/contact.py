from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract as DBManager
from auth_service.domain.contact import Contact
from auth_service.events import ContactEvent as Event


async def action_contact_save(event: Event, db_manager: DBManager):
    contact = Contact(user_id=event.user_id,
                      phone_number=event.phone_number,
                      first_name=event.first_name,
                      last_name=event.last_name)
    contact.is_valid_phone_number(phone_number=event.phone_number)
    await db_manager.contact_save(contact=contact)
    result = await db_manager.search_account(user_id=contact.user_id, phone_number=contact.phone_number)
    if result:
        return result
    return {"msg": "contact save"}


