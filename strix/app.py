"""
    strix.Application

    The application.
    Usage:
        import strix.app.Application


        class MyApplication(strix.app.Application):
            def __init__(self):
                pass
"""

from strix.router import Router


class Application():
    def __init__(self, handlers=None, **settings):
        self._router = Router(handlers)
        self.settings = self.get_settings(settings)
        if self.settings.get("static_path", None):
            static_path = self.settings["static_path"]
            static_url_prefix = self.settings.get("static_url_prefix", "/static/")

        if self.settings.get("debug", False):
            self.settings["autoreload"] = True
            self.settings["stack_traceback"] = True

    @property
    def log_access(self):
        pass

    @property
    def debug(self):
        return self.settings.get("debug", False)

    @property
    def route_map(self):
        return self._router

    @property
    def traceback_flag(self):
        return self.settings.get("stack_traceback", False)

    def get_settings(self, settings):
        tmp = {key.lower(): val for key, val in settings.items()}
        return tmp
