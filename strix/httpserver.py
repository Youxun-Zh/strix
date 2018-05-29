"""
    strix.httpserver

    This module implements the .

"""

import asyncio
import functools
import gc
import os
import signal
import uvloop
from functools import partial
from http import HTTPStatus

from strix.httplib import HTTPRequest, HTTPResponse
from strix.httplib.exceptions import HTTPError, HTTPParserError
from strix.httputils import parser_adapter, parser_http_header
from strix.protocol import HTTPProtocol

MAX_REQUEST_SIZE = 50 * (1<<20)


class HTTPServer():
    def __init__(self, app, host, port):
        # import ipdb; ipdb.set_trace()
        self.app = app
        self.debug = self.app.debug
        self.host = host
        self.port = port
        self.route_map = self.app._router
        # self.static_path = static_path
        # self.templates_path = templates_path
        self.loop = uvloop.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def is_running(self):
        return self.loop.is_running()

    # def on_exit(self, signame, http_server):
    def on_exit(self, signame, http_server):
        pid = os.getpid()
        exit_msg = "Pid [{pid}] exit".format(pid=pid)
        print(exit_msg)
        self.loop.stop()

    def add_signal_handler(self, http_server):
        signames = ("SIGINT", "SIGTERM")
        for signame in signames:
            self.loop.add_signal_handler(getattr(signal, signame),
                                         functools.partial(self.on_exit, signame, http_server))
                                         # functools.partial(self.on_exit, signame, http_server, server))

    def run(self):
        # import ipdb; ipdb.set_trace()
        print("* Running on http://{}:{}/ ".format(self.host, self.port))
        protocol = partial(HTTPProtocol, app=self.app, loop=self.loop)
        server_params = (protocol, self.host, self.port)
        self.coro = self.loop.create_server(*server_params)
        if self.debug:
            self.loop.set_debug(self.debug)
        http_server = self.loop.run_until_complete(self.coro)
        self.add_signal_handler(http_server)

        try:
            self.loop.run_forever()
        finally:
            gc.collect()
            http_server.close()
            self.loop.run_until_complete(http_server.wait_closed())

            self.loop.close()
