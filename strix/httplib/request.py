import base64
import copy
import datetime
import hashlib

from http import cookies
from urllib import parse


class HTTPRequest():
    # __slots__ = []

    def __init__(self, request_line, headers):
        self.request = request_line
        self.method = self.request.method
        self._data = {}
        self._arguments = {}
        self.url = self._parser_url()
        self.headers = self._parser_headers(headers)
        # self.get_host = self._parser_http_headers(header)
        # self.remote_addr = self._get_client_ip()
        self.form_data = {}
        self.body = {}
        self.XHR_flag = 'XMLHttpRequest'
        self._cookie = cookies.SimpleCookie(self.headers.get("Cookie"))

    def get_argument(self, arg, default=None):
        value = self._arguments.get(arg, default)
        return value

    def get_data(self, arg, default=None):
        if not hasattr(self, "_data"):
            self._data = {}
        return self._data.get(arg, default)

    def get_header(self, name, default=None):
        header = self.headers.get(name, default)
        return header

    def _parser_headers(self, headers):
        kvs = []
        content_length = "-1"
        for index, line in enumerate(headers):
            if line:
                if "application/x-www-form-urlencoded" in line or ("multipart/form-data" in line and "boundary" not in line):
                    kvs.append(line.split(": ", 1))

                    # cl = headers[index+1].split(": ", 1)
                    # kvs.append(cl)
                    # content_length = cl[1]
                    # length = int(content_length) if content_length.isdigit() else -1
                    # form_data = headers[index+3][:length]
                    # form_data = parse.unquote(form_data)
                    # form_data = parse.urlparse("?{}".format(form_data))
                    # self._data = dict(parse.parse_qsl(form_data.query))
                    # break
                elif "Content-Length" in line:
                    line = line.split(": ", 1)
                    kvs.append(line)
                    content_length = line[1]
                elif index+1 == len(headers):
                    length = int(content_length) if content_length.isdigit() else -1
                    form_data = line[:length]
                    form_data = parse.unquote(form_data)
                    form_data = parse.urlparse("?{}".format(form_data))
                    self._data = dict(parse.parse_qsl(form_data.query))
                elif "multipart/form-data" in line and "boundary" in line:
                    pass
                else:
                    data = line.split(": ", 1)
                    if data not in kvs:
                        kvs.append(data)

        return dict(kvs)

    def get_cookie(self, name):
        c = self._cookie.get(name)
        value = c.value if c else ""
        return value

    def get_secure_cookie(self, name, cookie_secret):
        # expire: timestamp
        raw_cookie_value = self.get_cookie(name)
        cookie_value = base64.b64decode(raw_cookie_value)
        if not cookie_value:
            value = ""
        else:
            value, expire, sign = cookie_value.decode().split(":")
            msg = "{}{}{}".format(value, str(expire), cookie_secret)
            raw_sign = hashlib.sha1(msg.encode()).hexdigest()
            if raw_sign != sign:
                value = ""
            now = datetime.datetime.now()
            if now > datetime.datetime.fromtimestamp(float(expire)):
                value = ""
        return value

    def _parser_url(self):
        # Generate query_params, query_string and url.
        # Unquote the url.
        url = parse.unquote(self.request.path)
        result = parse.urlparse(url)
        self.url, self.query_string = result.path, result.query
        self._arguments = dict(parse.parse_qsl(self.query_string))
        self.query_params = copy.deepcopy(self._arguments)
        return url

    @property
    def is_ajax(self):
        xhr_flag = self.http_headers.get('HTTP_X_REQUESTED_WITH')
        return xhr_flag == self.XHR_flag
