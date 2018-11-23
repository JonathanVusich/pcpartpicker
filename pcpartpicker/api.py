from .handler import Handler


class API:

    def __init__(self, region: str="us"):
        self._handler = Handler(region)

    @property
    def supported_regions(self):
        return self._handler._regions

    @property
    def supported_parts(self):
        return self._handler._supported_parts

    @property
    def region(self):
        return self._handler._region

    def set_region(self, region: str):
        self._handler._set_region(region)

    def retrieve(self, *args, force_refresh=False):
        return self._handler._retrieve(*args, force_refresh=force_refresh)

    def retrieve_all(self, force_refresh=False):
        return self._handler._retrieve(*self._handler._supported_parts, force_refresh=force_refresh)

