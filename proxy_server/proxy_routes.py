from typing import Optional

from aiohttp import web

from forwarder.forward import Forwarder, extract_payloads
from forwarder.timer import RequestTimer
from database.methods import update_request_metrics


async def forward_request(request: web.Request, proxy: Optional[str]=None):
    target_url = request._message.url
    target_method = request._message.method
    forward_req = Forwarder(target_url, target_method, request.headers)
    json_pay, data_pay = await extract_payloads(request)
    resp_bytes, response = await forward_req.forward(json=json_pay, data=data_pay, proxy=proxy)
    proxy_resp = web.Response(body=resp_bytes, status=response.status, headers=response.headers)
    proxy_resp._cookies = response.cookies
    return proxy_resp


async def server_proxy(request: web.Request):
    return await forward_request(request, None)


async def round_robin(request: web.Request):
    with RequestTimer() as t:
        proxy_id, proxy = await request.app['manager'].round_robin()
        resp = await forward_request(request, proxy)
    await update_request_metrics(proxy_id, resp.status, t.latency)
    return resp