from http import HTTPStatus

from strix.httplib.response import HTTPResponse
# from strix.http import HTTPResponse


class HTTPError(Exception):
    """Exception thrown for an unsuccessful HTTP request.

    Attributes:

    * ``code`` - HTTP error integer error code, e.g. 404.  Error code 599 is
      used when no HTTP response was received, e.g. for a timeout.

    * ``response`` - `HTTPResponse` object, if any.

    Note that if ``follow_redirects`` is False, redirects become HTTPErrors,
    and you can look at ``error.response.headers['Location']`` to see the
    destination of the redirect.
    """
    def __init__(self, http_status):
        self._status = http_status
        self.code = self._status.value
        self.message = "HTTP {}: {}".format(self.code, self._status.name)
        # Exception.__init__(self, "HTTP {}: {}".format(self._code, self.message))
        self.content = ""

    def set_content(self, content):
        self.content = content

    @property
    def body(self):
        self.response = HTTPResponse()
        self.response.set_status(self._status)
        if self.content:
            self.response._set_content(self.content)
        return self.response.body


class HTTPParserError(Exception):
    def __init__(self):
        Exception.__init__(self, "HTTP data parser error")
        self.body = b"HTTP data parser error"
        self._status = HTTPStatus.BAD_REQUEST.value

    @property
    def body(self):
        self.response = HTTPResponse()
        self.response.set_status(HTTPStatus.BAD_REQUEST)
        return self.response.body
