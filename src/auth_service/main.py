import json
import jwt
from aiohttp import web

from auth_service.config import SECRET_KEY
# from auth_service.db_manager.auto_migrate import run_migrations
from auth_service.handlers import send_sms_user, verify_code, account_create, contacts_save, \
    get_account_by_id_or_phone_number, get_all_my_contact, get_my_account, save_all_contacts
from asyncio.log import logger


def json_error(status_code: int, exception: Exception) -> web.Response:
    message = str(exception)

    if hasattr(exception, "status_code"):
        status_code = exception.status_code

    if hasattr(exception, "message"):
        message = exception.message

    return web.Response(
        status=status_code,
        body=json.dumps({
            "error": exception.__class__.__name__,
            "detail": message
        }).encode("utf-8"),
        content_type="application/json")


@web.middleware
async def middleware_handler(request, handler) -> [json_error, web.Response]:
    try:
        response = await handler(request)
        if response.status == 404:
            return json_error(response.status, Exception(response.message))
        return response
    except web.HTTPException as ex:
        if ex.status == 404:
            return json_error(ex.status, ex)
        raise
    except Exception as e:
        logger.warning('Request {} has failed with exception: {}'.format(request, repr(e)))
        return json_error(500, e)


#
# async def check_token(app: web.Application, handler):
#     async def authenticate(request):
#         token = request.headers.get('Authorization')
#         token: str = token.split(' ')[1]
#         response = await handler(request)
#         if not token:
#             return web.json_response({'error': 'Missing token'}, status=401)
#         try:
#             print('sfdg')
#             print(jwt.decode(token, SECRET_KEY, algorithms=['HS256']), 'asfdsg')
#             decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#             # request['user'] = decoded_token
#         except jwt.InvalidTokenError as inv:
#             return json_error(500, inv)
#
#         return response
#
#     return authenticate


app = web.Application(middlewares=[middleware_handler])
app.add_routes([web.post('/api/v1.0/send-sms', send_sms_user)])
app.add_routes([web.post('/api/v1.0/verify-code', verify_code)])

app.add_routes([web.get('/api/v1.0/accounts', get_account_by_id_or_phone_number)])
app.add_routes([web.get('/api/v1.0/my-account', get_my_account)])
app.add_routes([web.post('/api/v1.0/accounts', account_create)])

app.add_routes([web.get('/api/v1.0/contacts', get_all_my_contact)])
app.add_routes([web.post('/api/v1.0/contacts', contacts_save)])
app.add_routes([web.post('/api/v1.0/contacts-save', save_all_contacts)])


def start():
    web.run_app(app, port=8083)
