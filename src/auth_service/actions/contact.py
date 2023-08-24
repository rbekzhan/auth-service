from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract as DBManager
from auth_service.domain.contact import Contact
from auth_service.events import ContactEvent as Event
from auth_service.events import ContactsEvent as EventSave


async def action_contact_save(event: Event, db_manager: DBManager):
    contact = Contact(user_id=event.user_id,
                      phone_number=event.phone_number,
                      first_name=event.name,
                      last_name=event.surname)
    contact.is_valid_phone_number(phone_number=event.phone_number)
    await db_manager.contact_save(contact=contact)
    result = await db_manager.search_contact_account(user_id=contact.user_id, phone_number=contact.phone_number)
    if result:
        return result
    return {"msg": "contact save"}


async def action_get_all_my_contact(user_id: str, db_manager: DBManager):
    return await db_manager.get_all_my_contact(user_id)


async def action_save_all_contacts(event, db_manager: DBManager):
    for i in event:
        for number in i.phone_number:
            contact = Contact(user_id=str(i.user_id),
                              phone_number=number,
                              first_name=i.name,
                              last_name=i.surname)
            await db_manager.contact_save(contact=contact)
