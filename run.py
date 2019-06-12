from proxy_server.server import ProxyServer


if __name__ == '__main__':
    p = ProxyServer('0.0.0.0', 8000)
    p.run_app()
