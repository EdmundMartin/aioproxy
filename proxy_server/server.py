import asyncio
import os

from aiohttp import web
from tortoise import Tortoise

from proxy_server.proxy_routes import server_proxy, round_robin, round_robin_minimum_reliability
from proxy_server.management_routes import management_router
from proxy_manager.manger import ProxyManager


class ProxyServer:

    PROXY_STRATEGIES = {
        'round_robin': round_robin,
        'server_proxy': server_proxy,
        'round_robin_reliability': round_robin_minimum_reliability
    }

    def __init__(self, host: str, port: int, loop=None):
        self.host = host
        self.port = port
        self.loop = loop if loop else asyncio.get_event_loop()

    async def create_app(self):
        app = web.Application()
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['database.models']}
        )
        await Tortoise.generate_schemas()
        app['manager'] = ProxyManager()
        app.router.add_route('*', '/', self.PROXY_STRATEGIES.get(os.getenv('PROXY_STRATEGY',
                                                                           'round_robin_reliability')))
        app.add_routes(management_router)
        return app

    def run_app(self, ssl_context=None):
        loop = self.loop
        app = loop.run_until_complete(self.create_app())
        web.run_app(app, host=self.host, port=self.port, ssl_context=ssl_context)

