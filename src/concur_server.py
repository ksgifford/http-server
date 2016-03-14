"""A module that extends the server.py module to handle concurrent requests."""
# -*- coding: utf-8 -*-
from gevent.server import StreamServer
from gevent.monkey import patch_all
from server import server

ADDRESS = ("0.0.0.0", 5000)


if __name__ == "__main__":
    patch_all()
    server = StreamServer(ADDRESS, server)
    print("Starting StreamServer on ", ADDRESS)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print ("Connection Closing")
        server.close()
