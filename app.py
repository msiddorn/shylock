#!/usr/bin/python3
from sys import argv
from api.server import Server
from api.bottle_helpers import init_routes


if __name__ == '__main__':
    host = '0.0.0.0'
    port = int(argv[1])
    app = Server(host, port)
    init_routes(app)
    use_ssl = False if 'heroku' in argv else True
    app.start(use_ssl)
