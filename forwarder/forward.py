from typing import Dict, Tuple, Optional, Union

from aiohttp import ClientResponse, ClientSession
from aiohttp import web


async def _extract_bodies(request: web.Request) -> Tuple[Optional[Dict], Optional[Dict]]:
    methods = [(request.json, 'json'), (request.post, 'data')]
    for m in methods:
        try:
            method, res_type = m
            res = await method()
        except Exception:
            continue
        else:
            if res_type == 'json':
                return res, None
            return None, res
    return None, None


async def extract_payloads(request: web.Request) -> Tuple[Optional[Dict], Optional[Dict]]:
    if request.method in ['PUT', 'PATCH', 'POST'] and request.can_read_body:
        return await _extract_bodies(request)
    return None, None


class Forwarder:

    def __init__(self, location: str, method: str, headers):
        self.location = location
        self.method = method
        self.headers = headers

    async def forward(self, proxy: Optional[str]=None, data: Optional[Dict]=None,
                      json: Optional[Dict]=None, ) -> Tuple[bytes, ClientResponse]:
        async with ClientSession(headers=self.headers) as client:
            response = await client._request(self.method, self.location, proxy=proxy, json=json, data=data)
            resp_bytes = await response.read()
        return resp_bytes, response
