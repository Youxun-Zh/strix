def reverse():
    pass


def resolve():
    pass


def redirect(self, url, permanent=False, status=None):
    """Sends a redirect to the given (optionally relative) URL.

    If the ``status`` argument is specified, that value is used as the
    HTTP status code; otherwise either 301 (permanent) or 302
    (temporary) is chosen based on the ``permanent`` argument.
    The default is 302 (temporary).
    """
    if self._headers_written:
        raise Exception("Cannot redirect after headers have been written")
    if status is None:
        status = 301 if permanent else 302
    else:
        assert isinstance(status, int) and 300 <= status <= 399
    self.set_status(status)
    self.set_header("Location", utf8(url))
    self.finish()
