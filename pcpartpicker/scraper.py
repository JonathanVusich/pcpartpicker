from .errors import UnsupportedRegion

class Scraper:

    _supported_types = ["cpu"]
    _regions = ["au", "be", "ca", "de", "es", "fr",
                    "in", "ie", "it", "nz", "uk", "us"]
    _region = "us"
    _base_url = "http"

    def __init__(self, region: str="us"):
        self._set_region(region)


    @property
    def region(self) -> str:
        return self._region

    def _set_region(self, region: str):
        if not region in self._regions:
            raise UnsupportedRegion("Region \'{}\' is not supported!".format(region))
        self._region = region

    def _generate_url(self):
        if not region == "us":
            self._base_url = "https://{}.pcpartpicker.com".format(self._region)
