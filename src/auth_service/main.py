import json
import jwt
from aiohttp import web

from auth_service.config import SECRET_KEY
from auth_service.db_manager.auto_migrate import run_migrations
from auth_service.handlers import send_sms_user, verify_code, account_create, contacts_save
from asyncio.log import logger


def json_error(status_code: int, exception: Exception) -> web.Response:
    """
    Returns a Response from an exception.
    Used for error middleware.
    :param status_code:
    :param exception:
    :return:
    """
    return web.Response(
        status=status_code,
        body=json.dumps({
            'error': exception.__class__.__name__,
            'detail': str(exception)
        }).encode('utf-8'),
        # body=json.dumps({"error": "unidentified error"}).encode('utf-8'),
        content_type='application/json')


async def error_middleware(app: web.Application, handler):
    """
    This middleware handles with exceptions received from views or previous middleware.
    :param app:
    :param handler:
    :return:
    """

    async def middleware_handler(request):
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

    return middleware_handler

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


app = web.Application(middlewares=[error_middleware])
app.add_routes([web.post('/send-sms', send_sms_user)])
app.add_routes([web.post('/verify-code', verify_code)])
app.add_routes([web.post('/account-create', account_create)])
app.add_routes([web.post('/contact-save', contacts_save)])


def start():
    run_migrations()
    web.run_app(app, port=8083)
