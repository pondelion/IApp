from ..fred import FredCrawler


class GDPCrawler(FredCrawler):

    def _get_tag(self):
        return 'JPNNGDP'

    def _get_name(self):
        return 'gdp'
