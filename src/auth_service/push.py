import json
import typing as t

from aio_pika import Message, connect

from auth_service.config import RABBITMQ_AMQP


async def push(users: t.List, from_id: str, message: [t.Dict, str], self: bool = False) -> None:
    connection = await connect(RABBITMQ_AMQP)
    async with connection:
        channel = await connection.channel()
        for user in users:
            if self is False and user.user_id == from_id:
                continue
            queue = await channel.declare_queue(user.user_id)
            await channel.default_exchange.publish(
                Message(
                    json.dumps(message).encode()
                ), routing_key=queue.name)
