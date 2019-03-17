from .handler import Handler


class API:
    """API:

    This class is a wrapper class that allows for greater decoupling between
    the internals and the externally available functions.
    """

    def __init__(self, region: str = "us"):
        self._handler = Handler(region)

    @property
    def concurrent_connections(self):
        return self._handler._scraper._concurrent_connections

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
        """
        Public function that allows the user to change the region from which data will be fetched.

        :param region: str: The region
        :return: None
        """

        self._handler._set_region(region)

    def set_concurrent_connections(self, connections: int) -> None:
        """
        Public function that allows the user to change the number of concurrent connections to open
        to PCPartpicker. Higher values typically mean shorter scraping times, but also typically means
        a higher chance of the connection getting timed out. This value should most always be lowered.
        :param connections:
        :return:
        """
        self._handler._set_concurrent_connections(connections)

    def retrieve(self, *args, force_refresh=False):
        """
        Public function that allows the user to make part requests.

        :param args: str: Various string arguments that must be valid part types.
        :param force_refresh: bool: This value determines whether or not the API will used internally
        cached values (if available) or freshly acquired data.
        :return: dict: A dictionary that contains the requested parts as keys to their associated data object
        lists.
        """

        return self._handler._retrieve(*args, force_refresh=force_refresh)

    def retrieve_all(self, force_refresh=False):
        """
        Public function that allows the user to retrieve all supported part types.

        :param force_refresh: bool: This value determines whether or not the API will used internally
        cached values (if available) or freshly acquired data.
        :return: dict: A dictionary that contains all parts as keys to their associated data object
        lists.
        """

        return self._handler._retrieve(*self._handler._supported_parts, force_refresh=force_refresh)
