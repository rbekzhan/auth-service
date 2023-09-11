import typing

from auth_service.db_manager.auth_db_manager_abstract import AuthDBManagerAbstract as DBManager
from auth_service.domain.user import User
from auth_service.domain.user_profile import UserProfile
from auth_service.events import UserProfileEvent as Event


async def action_create_user_profile(event: Event, db_manager: DBManager):
    user: User = await db_manager.get_user_by_user_id(user_id=event.user_id)
    user_profile = UserProfile(
        user_id=event.user_id,
        username=event.username,
        name=event.name,
        surname=event.surname,
        email=event.email,
        avatar_path=event.avatar_path,
        bio=event.bio
    )
    user_profile.is_valid_username()
    user.set_profile(profile=user_profile)
    data: typing.Dict = await db_manager.save_user_state(user=user)

    return data["profile"]


async def action_check_username_profile(username: str, db_manager: DBManager):
    user_username = UserProfile(username=username)
    user_username.is_valid_username()

    return await db_manager.username_check(username=username)
