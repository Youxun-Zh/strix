import re
import traceback

from collections import namedtuple
from http import HTTPStatus
from urllib import parse

from strix.httplib.exceptions import HTTPError

_CRLF_RE = re.compile(r"\r?\n")


class HTTPHeaders(object):
    def __init__(self, headers):
        self.headers = headers

    def parse_form(self):
        pass

    def parse_query(self):
        pass


def parser_http_header(request_message, callback=None):
    """TODO:1.get, head url
            2.slash remove
    """
    if isinstance(request_message, bytes):
        request_message = request_message.decode()
    request_line, *headers = _CRLF_RE.split(request_message)

    request_line = parser_request_line(request_line)
    return request_line, headers

    # content_length = len(http_header)
    # headers = http_header.decode().split("\r\n")
    # request_line = headers[0]
    # headers_dict = {}
    # try:
    #     for item in headers[1:]:
    #         if not item:
    #             headers_dict["body"] = headers[-1]
    #             break
    #         key, val = item.split(": ")
    #         headers_dict[key] = val
    # except:
    #     raise HTTPParserError()
    # method, path, protocol = request_line.split(" ")
    # return method, path, protocol, headers_dict, content_length


def parser_request_line(request_line):
    method, path, version = request_line.split(" ")
    # try:
    #     method, path, version = request_line.split(" ")
    # except ValueError:
    #     raise HTTPInputError("Malformed HTTP request line")
    # if not re.match(r"^HTTP/1\.[0-1]$", version):
    #     raise HTTPInputError("Malformed HTTP version in HTTP Request-Line: %r" % version)
    RequestLine = namedtuple("RequestLine", ["method", "path", "version"])
    return RequestLine(method, path, version)


HANDLER_ATTRS = ("cookie_secret", )

def parser_adapter(route_map, app, request_line, headers, *args, **kwargs):
    # TODO: is or not remove slash
    parse_data = parse.urlparse(request_line.path)
    handler, h_kwargs = route_map.get_handler(parse_data.path)
    if not handler:
        response = HTTPError(HTTPStatus.NOT_FOUND)
    elif not hasattr(handler, request_line.method.lower()):
        response = HTTPError(HTTPStatus.METHOD_NOT_ALLOWED)
    else:
        handler_args = (request_line, headers)
        instance = handler(*handler_args)

        for attr in HANDLER_ATTRS:
            value = app.settings.get(attr, None)
            if value:
                setattr(instance, attr, value)
        # instance.response = HTTPResponse()
        func = getattr(instance, request_line.method.lower())

        try:
            response = func(**h_kwargs)
        except Exception as ex:
            # log
            if app.traceback_flag:
                response = HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR)
                traceback.print_exc()
                formatted_lines = traceback.format_exc()
                response.set_content(formatted_lines)
            else:
                response = HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR)
    return response

    return func, h_kwargs
