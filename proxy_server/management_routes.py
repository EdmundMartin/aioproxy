from aiohttp import web

from database.models import Proxy

management_router = web.RouteTableDef()


@management_router.post('/api/management/new-proxy')
async def add_new_proxy(request: web.Request):
    data = await request.json()
    await Proxy.create(ip=data.get('ip'), port=data.get('port'), is_https=data.get('https'))
    return web.json_response({'message': 'proxy added'}, status=200)


@management_router.post('/api/management/remove-proxy')
async def remove_proxy(request: web.Request):
    data = await request.json()
    proxy = await Proxy.filter(ip=data.get('proxy_ip')).first()
    await proxy.delete()
    return web.json_response({'message': 'proxy deleted'}, status=200)
