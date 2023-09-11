from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract as DBManager
from auth_service.domain.contact import Contact
from auth_service.domain.user import User
from auth_service.events import ContactEvent as Event


async def action_contact_save(event: Event, db_manager: DBManager):
    user: User = await db_manager.get_user_by_user_id(user_id=event.user_id)
    contact = Contact(
        user_id=event.user_id,
        phone_number=event.phone_number,
        name=event.name,
        surname=event.surname
    )
    user.add_contact(contact)
    contact.is_valid_phone_number(phone_number=event.phone_number)
    await db_manager.save_user_state(user=user)

    user: User = await db_manager.get_user_by_user_id(user_id=event.user_id)
    user.set_cursor_contact(contact=contact)
    current_contact: Contact = user.cursor_contact

    if current_contact.contact_profile is None:
        return {"msg": "contact save"}

    return {
        "user_id": current_contact.contact_profile.user_id,
        "username": current_contact.contact_profile.username,
        "name": current_contact.contact_profile.name,
        "surname": current_contact.contact_profile.surname,
        "avatar_path": current_contact.contact_profile.avatar_path,
        "bio": current_contact.contact_profile.bio
    }


async def action_get_all_my_contact(user_id: str, db_manager: DBManager):
    return await db_manager.get_all_my_contact(user_id)


async def action_save_all_contacts(user_id, event, db_manager: DBManager):
    user: User = await db_manager.get_user_by_user_id(user_id=user_id)
    for i in event:
        for number in i.phone_number:
            contact = Contact(user_id=i.user_id,
                              phone_number=number,
                              name=i.name,
                              surname=i.surname)
            user.add_contact(contact)
    await db_manager.save_user_state(user=user)
