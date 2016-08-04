'''
    System test for the webapi commands
    assumes server is running locally on port 9555 (make this an argument at some point)
    pytest order is made explicitly
'''
import pytest
import requests
import json
import re


address_prefix = 'http://0.0.0.0:9555/v1/'
json_header = {'Content-Type': 'application/json'}


@pytest.mark.order1
def test_home_page():
    r = requests.get(address_prefix[:-3])
    print(r.text)
    assert(json.loads(r.text) == 'hello world')

@pytest.mark.order2
def test_pools():
    results = []
    for pool_name in ['Paris', 'Rome']:
        results.append(requests.post(
            address_prefix + 'pools',
            data=json.dumps({'name': pool_name}),
            headers=json_header,
        ))
    assert(results[0].status_code == 200)
    assert(results[1].status_code == 200)

    pools = json.loads(requests.get(address_prefix + 'pools').text)
    assert(pools['0']['name'] == 'Paris')
    assert(pools['1']['name'] == 'Rome')

@pytest.mark.order3
def test_users():
    results = []
    for user_name in ['Mark', 'Sophie', 'Tom', 'Tom']:
        results.append(requests.post(
            address_prefix + '0/users',
            data=json.dumps({'name': user_name}),
            headers=json_header,
        ))
    results.append(requests.post(
        address_prefix + '99/users',
        data=json.dumps({'name': 'A person'}),
        headers=json_header,
    ))
    results.append(requests.get(address_prefix + '0/users'))
    for r in results[:3]:
        assert(r.status_code == 200)
    assert(results[3].status_code == 403)
    assert(results[4].status_code == 404)

    paris_users, rome_users, timbuktu_users = (
        requests.get(address_prefix + str(pool) + '/users')
        for pool in range(3)
    )
    assert(json.loads(paris_users.text) == ['Mark', 'Sophie', 'Tom'])
    assert(json.loads(rome_users.text) == [])
    assert(timbuktu_users.status_code == 404)

@pytest.mark.order4
def test_transactions():
    transactions = [
        ('0', {
            'spender': 'Mark',
            'amount': 30,
            'consumers': {'Mark': 1, 'Sophie': 1, 'Tom': 1},
        }),
        ('0', {
            'spender': 'Tom',
            'amount': 7.5,
            'consumers': {'Mark': 2, 'Sophie': 1},
        }),
        ('1', {
            'spender': 'Mark',
            'amount': 1,
            'consumers': {'Mark': 1, 'Sophie': 1, 'Tom': 1},
        }),
        ('0', {
            'spender': 'Mark',
            'consumers': {'Mark': 1, 'Sophie': 1, 'Tom': 1},
        }),
    ]
    results = [
        requests.post(
            address_prefix + pool + '/transactions',
            data=json.dumps(transaction),
            headers=json_header,
        )
        for pool, transaction in transactions
    ]
    assert(results[0].status_code == 200)
    assert(results[1].status_code == 200)
    assert(results[2].status_code == 404)
    assert(results[3].status_code == 400)

    seen_transactions = json.loads(requests.get(address_prefix + '0/transactions').text)
    for i, transaction in enumerate(seen_transactions):
        match = re.match('(\w+) spent ([0-9\.]+) on (\{.*\})', transaction)
        assert(match.groups()[0] == transactions[i][1]['spender'])
        assert(match.groups()[1] == str(transactions[i][1]['amount']))
        # Don't bother parsing consumers, the system tests are supposed to be just for the api

@pytest.mark.order5
def test_balances():
    balances = json.loads(requests.get(address_prefix + '0/balances').text)
    assert(balances['Mark'] == -15)
    assert(balances['Sophie'] == 12.5)
    assert(balances['Tom'] == 2.5)
