from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract as DBManager
from auth_service.domain.user_profile import UserProfile
from auth_service.events import UserProfileEvent as Event


async def action_create_user_profile(event: Event, db_manager: DBManager):
    user_profile = UserProfile(user_id=event.user_id, username=event.username, first_name=event.first_name,
                               last_name=event.last_name, avatar_path=event.avatar_path, bio=event.bio)
    user_profile.is_valid_username()
    result = await db_manager.create_account(user_profile=user_profile)
    return result
