import requests
import json
from sys import argv


if argv[1] == 'local':
    address_prefix = 'http://0.0.0.0:{}/v1/'.format(argv[2])
elif argv[1] == 'heroku':
    address_prefix = 'https://calm-brushlands-26293.herokuapp.com/v1/'


api_calls = [
    ('add new pool for paris trip', 'pools', {'name': 'Paris'}),
    ('add new pool for rome trip', 'pools', {'name': 'Rome'}),
    ('list pools', 'pools', None),
    ('Add Mark to Paris trip', '0/users', {'name': 'Mark'}),
    ('Add Sophie to Paris trip', '0/users', {'name': 'Sophie'}),
    ('Add Tom to Paris trip', '0/users', {'name': 'Tom'}),
    ('Try to add Tom to Paris trip again', '0/users', {'name': 'Tom'}),
    ('List users for Paris', '0/users', None),
    ('List users for Rome', '1/users', None),
    ('List users for Timbuktu', '2/users', None),
    (
        'Mark spends £30 on everyone',
        '0/transactions',
        {
            'spender': 'Mark',
            'amount': 30,
            'consumers': {
                'Mark': 1,
                'Sophie': 1,
                'Tom': 1,
            },
        }
    ),
    (
        'Tom buys sophie an ice cream and Mark a double cone',
        '0/transactions',
        {
            'spender': 'Tom',
            'amount': 7.5,
            'consumers': {
                'Mark': 2,
                'Sophie': 1,
            },
        }
    ),
    (
        'Mark tries to spend money for a pool he\'s not in',
        '1/transactions',
        {
            'spender': 'Mark',
            'amount': 1,
            'consumers': {
                'Mark': 1,
                'Sophie': 1,
            },
        }
    ),
    ('List the balances for the Paris trip', '0/balances', None),
    ('List the balances for the Rome trip', '1/balances', None),
    ('List all of the old transactions for the Paris trip', '0/transactions', None),
]

headers = {'Content-Type': 'application/json'}

for description, api_call, data in api_calls:
    print(description)
    address = address_prefix + api_call
    if data is None:
        print('Calling get on "{}"'.format(address))
        r = requests.get(address)
    else:
        print('Calling post on "{}" with {}'.format(address, data))
        r = requests.post(address, data=json.dumps(data), headers=headers)

    print('Response was:\n{}\n'.format(r.text))
