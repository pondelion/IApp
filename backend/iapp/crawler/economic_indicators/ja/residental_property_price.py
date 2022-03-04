from ..fred import FredCrawler


class ResidentalPropertyPriceCrawler(FredCrawler):

    def _get_tag(self):
        return 'QJPN628BIS'

    def _get_name(self):
        return 'residental_property_price'
