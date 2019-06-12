import requests

resp = requests.get('https://facebook.com', proxies={'http': 'http://0.0.0.0:8000/server-proxy'})
print(resp.headers)
print(resp.cookies)