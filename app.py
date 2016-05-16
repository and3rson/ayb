#!/usr/bin/env python2

from gevent import monkey
monkey.patch_all

from gevent import socket, pool
from gevent.server import StreamServer
from handler import Handler


server = StreamServer(('0.0.0.0', 11111), Handler.handle, spawn=pool.Pool(1000))
server.serve_forever()
