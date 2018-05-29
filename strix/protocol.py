import asyncio
import httptools

from strix.httplib.response import HTTPResponse
from strix.httplib.exceptions import HTTPError
from strix.httputils.helper import parser_adapter, parser_http_header


MAX_REQUEST_SIZE = 50 * (1<<20)

class HTTPProtocol(asyncio.Protocol):
    def __init__(self, app, loop):
        self.app = app
        self.route_map = self.app.route_map
        self.traceback_flag = self.app.traceback_flag
        self.loop = loop
        self.max_request_size = MAX_REQUEST_SIZE
        self.transports = set()
        self.response = HTTPResponse()

    def connection_made(self, transport):
        print("connection made")
        print(transport.get_extra_info("peername"))
        # import ipdb; ipdb.set_trace()
        self.transport = transport
        self.transports.add(transport)

    def connection_lost(self, exc):
        # import ipdb; ipdb.set_trace()
        print("connection lost")
        # self.transports.discard(self.transport)
        self.transports.discard(self)

    def data_received(self, data):
        # self.parser = httptools.parser.HttpRequestParser(self)
        # self.parser.feed_data(data)

        # payload_size = len(data)
        # if payload_size > self.max_request_size:
        #     response = HTTPError(HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
        # else:
        #     args = parser_http_header(data)
        #     response = parser_adapter(self.route_map, self.app, *args)

        # self.transport.write(response.body)
        self.transport.write(data)
        self.transport.close()

    def request(self):
        pass

    async def request_handler(self, *args):
        pass

    def on_message_complete(self):
        print("test on_message_complete")
        self.loop.create_task(self.request_handler(self.request, self.write_response))

    def write_response(self, response):
        print("response is %s" % respone)
        self.transport.write(b"end.............\r\n")

    async def stream_response(self, response):
        self.transport.write(b"end transport.............\r\n")
        self.transport.close()
