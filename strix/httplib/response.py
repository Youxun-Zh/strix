import base64
import datetime
import hashlib
import http
import time

from collections import OrderedDict
from http import HTTPStatus

from strix import utils


class HTTPResponse():
    def __init__(self, context=""):
        self.all_http_status = self._get_all_http_status()
        self.headers = {}
        self.context = context
        self.content = ""
        self.status_line = ""
        self._cookie = http.cookies.SimpleCookie()
        self._status_code = HTTPStatus.OK.value
        self._reason_phrase = HTTPStatus.OK.name
        self._version = "HTTP/1.1"

    def _get_all_http_status(self):
        all_http_status = dict(((http_status.value, http_status.phrase) for http_status in list(http.HTTPStatus)))
        return all_http_status

    def set_cookie(self, name, value, domain=None, expires=None, path="/", expires_days=None, **kwargs):
        if not hasattr(self, "_cookie"):
            self._cookie = http.cookies.SimpleCookie()
        if name in self._cookie:
            del self._new_cookie[name]
        self._cookie[name] = value
        morsel = self._cookie[name]
        if domain:
            morsel["domain"] = domain
        if expires_days is not None and not expires:
            expires = datetime.datetime.utcnow() + datetime.timedelta(
                days=expires_days)
        if expires:
            expires = expires.timestamp()
            morsel["expires"] = utils.format_timestamp(expires)
        if path:
            morsel["path"] = path
        for k, v in kwargs.items():
            if k == 'max_age':
                k = 'max-age'

            # skip falsy values for httponly and secure flags because
            # SimpleCookie sets them regardless
            if k in ['httponly', 'secure'] and not v:
                continue

            morsel[k] = v

    def set_secure_cookie(self, name, value, domain=None, expires=None, path="/", expires_days=14, **kwargs):
        cookie_secret = kwargs.get("cookie_secret", "")
        if cookie_secret:
            self.set_cookie(name, gen_signed_cookie_value(value, expires_days, cookie_secret))
        else:
            pass

    def clear_cookie(self, name, path="/", domain=None):
        """Deletes the cookie with the given name.

        Due to limitations of the cookie protocol, you must pass the same
        path and domain to clear a cookie as were used when that cookie
        was set (but there is no way to find out on the server side
        which values were used for a given cookie).
        """
        expires = datetime.datetime.utcnow() - datetime.timedelta(days=365)
        self.set_cookie(name, value="", path=path, expires=expires,
                        domain=domain)

    def set_header(self, name, value):
        self.headers[name] = value

    def set_status_line(self, version, http_status=HTTPStatus.OK):
        status_line_parts = {"version": version,
                             "status_code": http_status.value,
                             "reason_phrase": http_status.name}
        self.status_line = "{version} {status_code} {reason_phrase}\r\n".format(**status_line_parts)
        return self.status_line

    def set_version(self, version):
        self._version = version

    def set_status(self, status=HTTPStatus.OK):
        self._status_code = status.value
        self._reason_phrase = status.name

    def _get_status_line(self):
        if self._version is None:
            self._version = "HTTP/1.1"
        return "{} {} {}\r\n".format(*(self._version, self._status_code, self._reason_phrase))

    def _set_content(self, content):
        self.content = content

    @property
    def header_fields(self):
        headers = self.headers
        cookies = self._cookie
        headers["DATE"] = utils.format_timestamp(time.time())
        headers["Content-Length"] = len(self.message_body)
        headers = ["{}: {}".format(header, value) for header, value in headers.items()]
        if cookies:
            headers.append(cookies.output())
        headers = "\r\n".join(headers)
        return headers

    @property
    def message_body(self):
        if not self.context:
            self.context = "HTTP {}: {}\n".format(self._status_code, self._reason_phrase)
        if self.content:
            self.context += self.content
        return self.context

    @property
    def body(self):
        status_line = self._get_status_line()
        resp_parts = {"status_line": status_line,
                      "header_fields": self.header_fields,
                      "message_body": self.message_body}
        response_data = "{status_line}{header_fields}\r\n\r\n{message_body}\r\n".format(**resp_parts)
        return response_data.encode()

    def redirect(self, url, permanent=False, status=None):
        """Sends a redirect to the given (optionally relative) URL.
    
        If the ``status`` argument is specified, that value is used as the
        HTTP status code; otherwise either 301 (permanent) or 302
        (temporary) is chosen based on the ``permanent`` argument.
        The default is 302 (temporary).
        """
        # if self._headers_written:
        #     raise Exception("Cannot redirect after headers have been written")
        if status is None:
            status = HTTPStatus.MOVED_PERMANENTLY if permanent else HTTPStatus.FOUND
        # else:
        #     assert isinstance(status, int) and 300 <= status <= 399
        self.set_status(status)
        self.set_header("Location", url)


def gen_signed_cookie_value(value, expires_days, cookie_secret=""):
    now = datetime.datetime.now()
    expires_date = now + datetime.timedelta(days=expires_days)
    ts = int(expires_date.timestamp())
    msg = "{}{}{}".format(str(value), str(ts), cookie_secret)
    sign = hashlib.sha1(msg.encode()).hexdigest()
    raw_cookie_value = "{}:{}:{}".format(value, ts, sign)
    cookie_value = base64.b64encode(raw_cookie_value.encode())
    return cookie_value.decode()
