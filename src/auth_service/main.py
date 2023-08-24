import json
from aiohttp import web

from auth_service.handlers import send_sms_user, verify_code, account_create, contacts_save, get_all_my_contact
from auth_service.handlers import get_account_by_id_or_phone_number, get_my_account, save_all_contacts
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


app = web.Application(middlewares=[middleware_handler])
app.add_routes([web.post('/api/v1.0/send-sms', send_sms_user)])
app.add_routes([web.post('/api/v1.0/verify-code', verify_code)])

app.add_routes([web.get('/api/v1.0/accounts', get_account_by_id_or_phone_number)])
app.add_routes([web.get('/api/v1.0/profiles', get_my_account)])
app.add_routes([web.post('/api/v1.0/accounts', account_create)])

app.add_routes([web.get('/api/v1.0/contacts', get_all_my_contact)])
app.add_routes([web.post('/api/v1.0/contacts', contacts_save)])
app.add_routes([web.post('/api/v1.0/contacts-save', save_all_contacts)])


def start():
    web.run_app(app, port=60004)
