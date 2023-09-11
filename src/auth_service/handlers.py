import json
import typing as t

from aiohttp import web
from auth_service.actions.contact import action_contact_save, action_get_all_my_contact, action_save_all_contacts
from auth_service.actions.get_account import action_search_account_by_id_or_phone_number, action_get_my_account
from auth_service.actions.user_profile import action_create_user_profile, action_check_username_profile
from auth_service.db_manager.auth_db_manager import DBManager
from auth_service.actions.send_verify_sms import action_create_sms, action_verify_sms, action_refresh_token, \
    action_logout_token
from auth_service.events import VerifyCodeEvent, UserProfileEvent, ContactEvent, ContactsEvent
from auth_service.helper import extract_user_id_from_token
from auth_service.schemas import VerifyCodeSchema, UserProfileSchema, ContactSchema, ContactsSaveSchema


# TODO перебрать код по Exception

async def send_sms_user(request: web.Request) -> json:
    body: t.Dict = await request.json()
    await action_create_sms(phone_number=body['phone_number'], db_manager=DBManager())
    return web.json_response(data={
        "msg": "success"
    })


async def verify_code(request: web.Request):
    event: VerifyCodeEvent = VerifyCodeSchema().load(data=await request.json())
    token = await action_verify_sms(event, db_manager=DBManager())

    return web.json_response(data=token)


async def refresh_token_pair(request: web.Request):
    token = request.headers.get('Authorization')
    if token is None:
        return web.json_response(data={"msg": "token required"})
    token = token.split(' ')[1]
    new_token = await action_refresh_token(token)
    return web.json_response(data=new_token)


async def sign_out(request: web.Request):
    token = request.headers.get('Authorization')
    if token is None:
        return web.json_response(data={"msg": "token required"})
    user_id = extract_user_id_from_token(token)
    token: str = token.split(' ')[1]
    await action_logout_token(token, user_id)
    return web.json_response(data={"msg": "Sign out"})


async def account_create(request: web.Request):
    token = request.headers.get('Authorization')
    if token is None:
        return web.json_response(data={"msg": "token required"})
    user_id = extract_user_id_from_token(token)
    data = await request.json()
    data['user_id'] = user_id
    event: UserProfileEvent = UserProfileSchema().load(data=data)
    user_profile = await action_create_user_profile(event, db_manager=DBManager())
    return web.json_response(data=user_profile)


async def username_check(request: web.Request):
    body = await request.json()
    username_status = await action_check_username_profile(**body, db_manager=DBManager())
    return web.json_response(data=username_status)


async def contacts_save(request: web.Request):
    token = request.headers.get('Authorization')
    if token is None:
        return web.json_response(data={"msg": "token required"})
    user_id = extract_user_id_from_token(token)
    data = await request.json()
    data['user_id'] = user_id
    event: ContactEvent = ContactSchema().load(data=data)
    contact = await action_contact_save(event, db_manager=DBManager())
    return web.json_response(data=contact)


async def get_account_by_id_or_phone_number(request: web.Request):
    user_id = request.query.get('user_id')
    phone_number = request.query.get('phone_number')
    result = await action_search_account_by_id_or_phone_number(user_id=user_id,
                                                               phone_number=phone_number,
                                                               db_manager=DBManager())
    return web.json_response(data=result)


async def get_all_my_contact(request: web.Request):
    token = request.headers.get('Authorization')
    if token is None:
        return web.json_response(data={"msg": "token required"})
    user_id = extract_user_id_from_token(token)
    result = await action_get_all_my_contact(user_id=user_id, db_manager=DBManager())
    return web.json_response(data=result)


async def get_my_account(request: web.Request):
    token = request.headers.get('Authorization')
    if token is None:
        # TODO: создать отдельный exception
        raise ValueError("token required")
    user_id = extract_user_id_from_token(token)
    result: t.Dict = await action_get_my_account(user_id=user_id, db_manager=DBManager())
    return web.json_response(data=result)


async def save_all_contacts(request: web.Request):
    token = request.headers.get('Authorization')
    if token is None:
        return web.json_response(data={"msg": "token required"})
    user_id = extract_user_id_from_token(token)
    body: t.Dict = await request.json()
    contacts = body.get('contacts', None)

    events: t.List[ContactsEvent] = []
    for contact in contacts:
        event: ContactsEvent = ContactsSaveSchema().load(data=contact | {"user_id": user_id})
        events.append(event)
    await action_save_all_contacts(user_id=user_id, event=events, db_manager=DBManager())
    return web.json_response(data={'msg': 'contacts saved'})
