

def to_proxy_format(ip: str, port: int, https: bool):
    scheme = 'https' if https else 'http'
    return '{}://{}:{}'.format(scheme, ip, port)


class ProxyMonitor:

    def __init__(self, id: int, ip: str, port: int, https: bool):
        self.id = id
        self.proxy = to_proxy_format(ip, port, https)
        self.https = https

    async def monitor_proxy(self):
        pass