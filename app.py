#!/usr/bin/python3
from api.server import Server
from api.bottle_helpers import init_routes
from sys import argv


if __name__ == '__main__':
    app = Server('0.0.0.0', argv[1])
    init_routes(app)
    app.start()
