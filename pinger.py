import requests



url = input('Endpoint:')

while True:
    params = input('params:')
    requests.get(url+params)
