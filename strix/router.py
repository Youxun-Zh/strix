import re

from functools import lru_cache


class Router():
    def __init__(self, urls):
        self.route_map = urls

    @lru_cache(maxsize=None)
    def get_handler(self, url):
        callback, kwargs = None, {}
        for pattern, handler in self.route_map:
            pattern = re.compile(pattern)
            result = re.search(pattern, url)
            if result:
               callback = handler
               kwargs.update(result.groupdict())
               break
        return callback, kwargs


def resolve(self):
    pass


def sverse(self):
    pass


def redirect():
    pass
