import json
import typing as t
import aiohttp_cors

from aiohttp import web
from asyncio.log import logger
from aiomisc.service.aiohttp import AIOHTTPService


def json_error(status_code: int, exception: Exception) -> web.Response:

    message = str(exception)
    code = -1

    if hasattr(exception, "status_code"):
        status_code = exception.status_code

    if hasattr(exception, "message"):
        message = exception.message

    if hasattr(exception, "code"):
        code = exception.code

    return web.Response(
        status=status_code,
        body=json.dumps({
            "detail": message,
            "code": code
        }).encode("utf-8"),
        content_type="application/json")


@web.middleware
async def error_middleware(request, handler) -> [json_error, web.Response]:
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


class GateWayService(AIOHTTPService):
    def __init__(self, routes: t.List, **kwargs):
        self._routes = routes
        super().__init__(**kwargs)

    async def create_application(self):
        app = web.Application(middlewares=[error_middleware])
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        app.add_routes(self._routes)

        for route in list(app.router.routes()):
            cors.add(route)

        return app
