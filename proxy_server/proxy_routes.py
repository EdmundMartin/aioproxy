from typing import Optional

from aiohttp import web
from aiohttp.client_exceptions import ClientError

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
        try:
            resp = await forward_request(request, proxy)
        except ClientError:
            status = 100
            resp = web.json_response({'error': 'unable to make request'}, status=500)
        else:
            status = resp.status
    await update_request_metrics(proxy_id, status, t.latency)
    return resp


async def round_robin_minimum_reliability(request: web.Request):
    with RequestTimer() as t:
        print('LOL')
        proxy_id, proxy = await request.app['manager'].round_robin_reliability()
        try:
            resp = await forward_request(request, proxy)
        except ClientError:
            status = 100
            resp = web.json_response({'error': 'unable to make request'}, status=500)
        else:
            status = resp.status
    await update_request_metrics(proxy_id, status, t.latency)
    return resp
