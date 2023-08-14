import pytest

from auth_service.actions.user_profile import action_create_user_profile
from auth_service.domain.user_profile import UserProfile
from auth_service.events import UserProfileEvent
from auth_service.exception import UsernameLengthCheck, EnglishLettersOnly, UsernameFormatCheck
from conftest import MockDBManager


@pytest.mark.asyncio
async def test_english_letter_user_profile_username():
    user_id = '2b2d45e4-2192-4cfb-a551-ad2066a019e8'
    user_profile = UserProfile(user_id=user_id, username='1вапавы4', first_name='Kostya', last_name='Katnikov')
    with pytest.raises(EnglishLettersOnly, match='username должна состоит из английских букв'):
        user_profile.is_valid_username()


@pytest.mark.asyncio
async def test_len_username():
    user_id = '2b2d45e4-2192-4cfb-a551-ad2066a019e8'
    user_profile = UserProfile(user_id=user_id, username='beka', first_name='Kostya', last_name='Katnikov')
    with pytest.raises(UsernameLengthCheck, match='Мало символа'):
        user_profile.is_valid_username()


@pytest.mark.asyncio
async def test_len_username():
    user_id = '2b2d45e4-2192-4cfb-a551-ad2066a019e8'
    user_profile = UserProfile(user_id=user_id, username='123beka', first_name='Kostya', last_name='Katnikov')
    with pytest.raises(UsernameFormatCheck, match='первый символ не может быть цифрой'):
        user_profile.is_valid_username()


@pytest.mark.asyncio
async def test_insert_username():
    user_id = '2b2d45e4-2192-4cfb-a551-ad2066a019e8'
    user_profile = UserProfile(user_id=user_id, username='beka08', first_name='Kostya', last_name='Katnikov')
    assert isinstance(user_profile, UserProfile)


@pytest.mark.asyncio
async def test_action_create_user_profile():
    event = UserProfileEvent(
                            user_id='87077fbf-73ec-4f6c-8c72-13bf627d05be',
                            username='rbekzhan',
                            first_name='Bekzhan',
                            last_name='Rakhmetzhan',
                            bio='tester'
                            )

    result = await action_create_user_profile(event=event, db_manager=MockDBManager())
    assert isinstance(result, dict)
    assert result['last_name'] == 'Rakhmetzhan'
    assert result['first_name'] != 'Bekzhx'
    assert result['username'] == 'rbekzhan'

