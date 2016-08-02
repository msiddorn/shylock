#!/usr/bin/python3
from api.server import Server
from api.bottle_helpers import init_routes


if __name__ == '__main__':
    app = Server('0.0.0.0', 9555)
    init_routes(app)
    app.start()
