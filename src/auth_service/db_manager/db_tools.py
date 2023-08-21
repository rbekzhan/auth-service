import json
import logging
import aiohttp
import typing as t

from auth_service.config import LOGGING_FORMAT


class DBTools:
    logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)

    def __init__(self):
        self._log = logging.getLogger(__name__)

    async def db_get(self, url: str, params: t.Dict = None) -> t.Any:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, params=params) as resp:
                    result: t.Dict = await resp.json()
        except Exception as e:
            self._log.exception(e)
            raise ValueError("Something went wrong")

        return result

    async def db_post(self, url: str, payload: t.Dict) -> t.Any:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, data=json.dumps(payload)) as resp:
                    result_text = await resp.text()

                    # Проверяем, что ответ не пустой, прежде чем пытаться разобрать его как JSON
                    if result_text:
                        result: t.Dict = json.loads(result_text)
                    else:
                        result = {}
                    return result

        except Exception as e:
            self._log.exception(e)
            raise ValueError("Something went wrong")