#!/usr/bin/python3
'''
    Backend webapi for the shylock program
'''
from bottle import Bottle
from bottle_helpers import router, init_routes


class Server:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()

    def start(self):
        self._app.run(host=self._host, port=self._port)

    @router('GET', '/home')
    def hello(self):
        return 'this is a web site'


if __name__ == '__main__':
    app = Server('0.0.0.0', 9555)
    init_routes(app)
    app.start()

    
