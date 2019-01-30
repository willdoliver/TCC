import requests

from stem import Signal
from stem.control import Controller

response = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'})
response.text.strip()
 
with Controller.from_port(port=9051) as controller:
	controller.authenticate(password='my password')
	controller.signal(Signal.NEWNYM)

response = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'})
print(response.text.strip())
