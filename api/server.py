#!/usr/bin/python3
'''
    Backend webapi for the shylock program
'''
from bottle import Bottle, abort, static_file
from cherrypy.wsgiserver import CherryPyWSGIServer
from cherrypy.wsgiserver.ssl_builtin import BuiltinSSLAdapter
from itertools import count
from .bottle_helpers import webapi, picture
# from .postgres_helpers import Database
from backend import Pool, MemberNotFoundError, NoneUniqueMemberError


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ssl_cert = 'cert.pem'
        self.ssl_key = 'privkey.pem'
        self._app = Bottle()
        self.pool_ids = count(0)
        self.pools = {}  # with a simple count could be a list - but this supports any id's
        # self.db = Database()

    def start(self, use_ssl):
        try:
            if use_ssl:
                CherryPyWSGIServer.ssl_adapter = BuiltinSSLAdapter(
                    self.ssl_cert,
                    self.ssl_key,
                    None
                )
                server = CherryPyWSGIServer(
                    (self.host, self.port),
                    self._app,
                    server_name='SplitPotAPI',
                    numthreads=10
                )
                try:
                    server.start()
                except KeyboardInterrupt:
                    server.stop()
            else:
                self._app.run(host=self.host, port=self.port)
        finally:
            pass
            # self.db.teardown()

    @property
    def pools_dict(self):
        return {pool_id: pool.__dict__ for pool_id, pool in self.pools.items()}

    @webapi('GET', '/')
    def home_page(self):
        return 'hello world'

    @webapi('GET', '/v1/pools')
    def list_pools(self):
        return self.pools_dict

    @webapi('GET', '/v1/<pool_id>/members')
    def list_users(self, pool):
        return pool.members

    @webapi('GET', '/v1/<pool_id>/balances')
    def list_balances(self, pool):
        return {name: pool.balances.get(name, 0) for name in pool.members}

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

    @webapi('POST', '/v1/users')
    def create_new_user(self, pool):
        try:
            username = data['name']
            password = data['password']
        except KeyError:
            abort(400, 'POST data must contain both a username and a password')

        # err_code, msg = self.db.add_user(username, password)
        # if err_code is not None:
        #     abort(err_code, msg)

    @webapi('POST', '/v1/<pool_id>/members')
    def add_pool_member(self, pool, data):
        name = data.get('name')
        try:
            pool.add_member(name)
        except NoneUniqueMemberError as err:
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
        except MemberNotFoundError as err:
            abort(404, 'No such member in this pool')

    @picture('/images/avatar')
    def avatar(self):
        return static_file('avatar.jpg', 'images')
