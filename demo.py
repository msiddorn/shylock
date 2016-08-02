import requests
import json


api_calls = [
    ('pools', {'name': 'Paris'}),
    ('pools', {'name': 'Rome'}),
    ('pools', None),
]

headers = {'Content-Type': 'application/json'}

for api_loc, data in api_calls:
    address = 'http://0.0.0.0:9555/v1/{}'.format(api_loc)
    if data is None:
        print('Calling get on "{}"'.format(address))
        r = requests.get(address)
    else:
        print('Calling post on "{}" with {}'.format(address, data))
        r = requests.post(address, data=json.dumps(data), headers=headers)

    print('Response was:\n{}\n'.format(r.text))
