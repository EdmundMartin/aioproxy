import requests

resp = requests.get('http://ip.lol',
                    proxies={'http': 'http://127.0.0.1:8000'})
print(resp.headers)
print(resp.cookies)
print(resp.text)