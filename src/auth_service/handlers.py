import json
import typing

from aiohttp import web

from auth_service.actions.contact import action_contact_save, action_get_all_my_contact
from auth_service.actions.get_account import action_search_account_by_id_or_phone_number
from auth_service.actions.user_profile import action_create_user_profile
from auth_service.db_manager.auth_db_manager import DBManager

from auth_service.actions.send_verify_sms import action_create_sms, action_verify_sms
from auth_service.events import RegisterEvent, VerifyCodeEvent, UserProfileEvent, ContactEvent
from auth_service.helper import extract_user_id_from_token
from auth_service.schemas import VerifyCodeSchema, UserProfileSchema, ContactSchema


async def send_sms_user(request: web.Request) -> json:
    body: typing.Dict = await request.json()
    result: typing.Dict = await action_create_sms(phone_number=body['phone_number'], db_manager=DBManager())
    return web.json_response(data=result)


async def verify_code(request: web.Request):
    event: VerifyCodeEvent = VerifyCodeSchema().load(data=await request.json())
    token = await action_verify_sms(event, db_manager=DBManager())

    return web.json_response(data=token)


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
    body: typing.Dict = await request.json()
    result = await action_search_account_by_id_or_phone_number(user_id=body.get('user_id', None),
                                                               phone_number=body.get('phone_number', None),
                                                               db_manager=DBManager())
    return web.json_response(data=result)


async def get_all_my_contact(request: web.Request):
    token = request.headers.get('Authorization')
    if token is None:
        return web.json_response(data={"msg": "token required"})
    user_id = extract_user_id_from_token(token)
    result = await action_get_all_my_contact(user_id=user_id, db_manager=DBManager())
    return web.json_response(data=result)
