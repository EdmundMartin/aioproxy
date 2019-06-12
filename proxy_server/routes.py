from aiohttp import web

from forwarder.forward import Forwarder, extract_payloads


async def server_proxy(request: web.Request):
    target_url = request._message.url
    target_method = request._message.method
    forward_req = Forwarder(target_url, target_method, request.headers)
    json_pay, data_pay = await extract_payloads(request)
    resp_bytes, response = await forward_req.forward(json=json_pay, data=data_pay)
    proxy_resp = web.Response(body=resp_bytes, status=response.status, headers=response.headers,
                              content_type=response.content_type)
    proxy_resp._cookies = response.cookies
    return proxy_resp


async def use_random_proxy(request: web.Request):
    return