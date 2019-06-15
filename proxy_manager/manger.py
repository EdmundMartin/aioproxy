from random import choice
from typing import List, Tuple

from database.models import Proxy


def _format_proxy(choice: Tuple[str, int, bool]):
    schema = 'https' if choice[3] is True else 'http'
    return '{}://{}:{}'.format(schema, choice[1], choice[2])


class ProxyManager:

    def __init__(self):
        self.idx = 0

    async def round_robin(self) -> Tuple[int, str]:
        proxies: List[tuple] = await Proxy.all().values_list('id', 'ip', 'port', 'is_https')
        next_proxy = proxies[self.idx % len(proxies)]
        self.idx += 1
        return next_proxy[0], _format_proxy(next_proxy)

    async def random_choice(self) -> Tuple[int, str]:
        proxies: List[tuple] = await Proxy.all().values_list('id', 'ip', 'port', 'is_https')
        next_proxy = choice(proxies)
        return next_proxy[0], _format_proxy(next_proxy)

