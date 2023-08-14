from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract as DBManager


async def action_search_account_by_id_or_phone_number(user_id: None, phone_number: None, db_manager: DBManager):
    return await db_manager.search_account_by_id_or_phone_number(user_id=user_id, phone_number=phone_number)