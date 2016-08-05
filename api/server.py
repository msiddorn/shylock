#!/usr/bin/python3
'''
    Backend webapi for the shylock program
'''
from bottle import Bottle, abort, static_file
from itertools import count
from .bottle_helpers import webapi, picture
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

    @property
    def pools_dict(self):
        return {pool_id: pool.__dict__ for pool_id, pool in self.pools.items()}

    @webapi('GET', '/')
    def home_page(self):
        return 'hello world'

    @webapi('GET', '/v1/pools')
    def list_pools(self):
        return self.pools_dict

    @webapi('GET', '/v1/<pool_id>/users')
    def list_users(self, pool):
        return pool.users

    @webapi('GET', '/v1/<pool_id>/balances')
    def list_balances(self, pool):
        return {name: pool.balances.get(name, 0) for name in pool.users}

    @webapi('GET', '/v1/<pool_id>/transactions')
    def list_transactions(self, pool):
        return [
            '{0[spender]} spent {0[amount]} on {0[consumers]}'.format(transaction)
            for transaction in pool.old_transactions
        ]

    @webapi('POST', '/v1/pools')
    def create_new_pool(self, data):
        name = data.get('name')
        pool_id = str(next(self.pool_ids))
        self.pools[pool_id] = Pool(name)

    @webapi('POST', '/v1/<pool_id>/users')
    def add_new_user(self, pool, data):
        name = data.get('name')
        try:
            pool.add_user(name)
        except NoneUniqueUserError as err:
            abort(403, 'Duplicate names would be confusing and are not allowed')

    @webapi('POST', '/v1/<pool_id>/transactions')
    def create_new_transaction(self, pool, data):
        try:
            spender = data['spender']
            amount = data['amount']
            consumers = data['consumers']
        except KeyError:
            abort(400, 'Need a sender, and amount, and consumers')

        try:
            pool.add_transaction(spender, amount, consumers)
        except UserNotFoundError as err:
            abort(404, 'No such user in this pool')

    @picture('/images/avatar')
    def avatar(self):
        return static_file('avatar.jpg', 'images')
