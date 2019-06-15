import asyncio
from typing import Dict

from database.models import Proxy


def _update_state(status_code: int, state: Dict) -> None:
    state['requests_made'] += 1
    if status_code >= 500:
        state['status_5xx'] += 1
        return
    elif status_code >= 400:
        state['status_4xx'] += 1
        return
    elif status_code >= 200:
        state['status_2xx'] += 1


async def _update_request_metrics(proxy_id: int, status_code: int, latency: float) -> None:
    proxy = await Proxy.filter(id=proxy_id).first()
    state = {'requests_made': proxy.requests_made, 'status_2xx': proxy.status_2xx, 'status_4xx': proxy.status_4xx,
             'status_5xx': proxy.status_5xx, 'request_latency': latency, 'requests_stability': proxy.requests_stability}
    _update_state(status_code, state)
    state['requests_stability'] = state['status_2xx'] / state['requests_made']
    await Proxy.filter(id=proxy_id).update(**state)


async def update_request_metrics(proxy_id: int, status_code: int, latency: float) -> None:
    loop = asyncio.get_event_loop()
    loop.create_task(_update_request_metrics(proxy_id, status_code, latency))