from random import choice
from typing import List, Tuple

from database.models import Proxy


def _format_proxy(choice: Tuple[str, int, bool]):
    schema = 'https' if choice[3] is True else 'http'
    return '{}://{}:{}'.format(schema, choice[1], choice[2])


class ProxyManager:

    def __init__(self, minimum_reliability: float = 0.9):
        self.idx = 0
        self.minimum_reliability = minimum_reliability

    async def round_robin(self) -> Tuple[int, str]:
        proxies: List[tuple] = await Proxy.all().values_list('id', 'ip', 'port', 'is_https')
        next_proxy = proxies[self.idx % len(proxies)]
        self.idx += 1
        return next_proxy[0], _format_proxy(next_proxy)

    async def round_robin_reliability(self) -> Tuple[int, str]:
        proxies = await Proxy.filter(requests_stability__gte=self.minimum_reliability).all().values_list()
        if len(proxies) > 0:
            next_proxy = proxies[self.idx % len(proxies)]
            self.idx += 1
            return next_proxy[0], _format_proxy(next_proxy)
        return await self.round_robin()

    async def random_choice(self) -> Tuple[int, str]:
        proxies: List[tuple] = await Proxy.all().values_list('id', 'ip', 'port', 'is_https')
        next_proxy = choice(proxies)
        return next_proxy[0], _format_proxy(next_proxy)

