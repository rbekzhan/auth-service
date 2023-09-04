from aiomisc import entrypoint
from auth_service.route import routes
from auth_service.services.gate_way_service import GateWayService

services = (GateWayService(address="0.0.0.0", port=60009, routes=routes),)


def start():
    with entrypoint(*services) as loop:
        loop.run_forever()

