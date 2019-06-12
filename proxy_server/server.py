import asyncio

from aiohttp import web

from proxy_server.routes import server_proxy


class ProxyServer:

    def __init__(self, host: str, port: int, loop=None):
        self.host = host
        self.port = port
        self.loop = loop if loop else asyncio.get_event_loop()

    async def create_app(self):
        app = web.Application()
        app.router.add_route('*', '/server-proxy', server_proxy)
        return app

    def run_app(self):
        loop = self.loop
        app = loop.run_until_complete(self.create_app())
        web.run_app(app, host=self.host, port=self.port)

