from aiohttp import web

from auth_service.handlers import send_sms_user, verify_code, get_account_by_id_or_phone_number, get_my_account, \
    refresh_token_pair, sign_out, username_check
from auth_service.handlers import account_create, contacts_save, save_all_contacts, get_all_my_contact

routes = [
    web.post('/api/v1.0/send-sms', send_sms_user),
    web.post('/api/v1.0/verify-code', verify_code),
    web.post('/api/v1.0/refresh', refresh_token_pair),
    web.post('/api/v1.0/sign-out', sign_out),

    web.get('/api/v1.0/profiles', get_account_by_id_or_phone_number),
    web.post('/api/v1.0/profiles/username-check', username_check),
    web.get('/api/v1.0/my/profiles', get_my_account),
    web.post('/api/v1.0/my/profiles', account_create),

    web.get('/api/v1.0/contacts', get_all_my_contact),
    web.post('/api/v1.0/contact', contacts_save),
    web.post('/api/v1.0/contacts', save_all_contacts)
]
