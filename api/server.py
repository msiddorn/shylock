#!/usr/bin/python3
'''
    Backend webapi for the shylock program
'''
import json
from bottle import Bottle, request
from itertools import count
from .bottle_helpers import router
from backend import Pool, UserNotFoundError, NoneUniqueUserError


class Server:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()
        self.pool_ids = count(0)
        self.pools = {}  # with a simple count could be a list - but this supports any id's

    def start(self):
        self._app.run(host=self._host, port=self._port)

    @router('POST', '/v1/<pool_id>/users')
    def add_new_user(self, pool_id):
        try:
            pool = self.pools[pool_id]
        except KeyError:
            return 'Error - No such pool id\n'
        data = json.loads(request.body.read().decode('utf-8'))
        name = data.get('name')
        try:
            pool.add_user(name)
        except NoneUniqueUserError as err:
            return str(err)

        # return a 200 OK
        return 'done\n'

    @router('GET', '/v1/<pool_id>/users')
    def list_users(self, pool_id):
        try:
            pool = self.pools[pool_id]
        except KeyError:
            return 'Error - No such pool id\n'

        return ''.join('{}\n'.format(name) for name in pool.users)

    @router('GET', '/v1/<pool_id>/balances')
    def list_balances(self, pool_id):
        try:
            pool = self.pools[pool_id]
        except KeyError:
            return 'Error - No such pool id\n'

        return ''.join(
            '{}: {}£{:0.2f}\n'.format(name, '' if balance >= 0 else '-', abs(balance))
            for name, balance in pool.balances.items()
        )

    @router('POST', '/v1/pools')
    def create_new_pool(self):
        data = json.loads(request.body.read().decode('utf-8'))
        name = data.get('name')
        pool_id = str(next(self.pool_ids))
        self.pools[pool_id] = Pool(pool_id, name)

        # return a 200 OK
        return 'done\n'

    @router('GET', '/v1/pools')
    def list_pools(self):
        return ''.join('{}\n'.format(pool) for pool in self.pools.values())

    @router('POST', '/v1/<pool_id>/transactions')
    def create_new_transaction(self, pool_id):
        try:
            pool = self.pools[pool_id]
        except KeyError:
            return 'Error - No such pool id\n'
        data = json.loads(request.body.read().decode('utf-8'))
        try:
            spender = data['spender']
            amount = data['amount']
            consumers = data['consumers']
        except KeyError:
            return 'Error - I need all this information\n'

        try:
            pool.add_transaction(spender, amount, consumers)
        except UserNotFoundError as err:
            return str(err)

        # return a 200 OK
        return 'done\n'

    @router('GET', '/v1/<pool_id>/transactions')
    def list_transactions(self, pool_id):
        try:
            pool = self.pools[pool_id]
        except KeyError:
            return 'Error - No such pool id\n'

        return ''.join(
            '{0[spender]} spent {0[amount]} on {0[consumers]}\n'.format(transaction)
            for transaction in pool.old_transactions
        )
