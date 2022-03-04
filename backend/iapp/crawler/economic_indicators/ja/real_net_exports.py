from ..fred import FredCrawler


class RealNetExportsGoodServicesCrawler(FredCrawler):

    def _get_tag(self):
        return 'JPNRGDPNGS'

    def _get_name(self):
        return 'real_net_exports_of_good_and_services'
