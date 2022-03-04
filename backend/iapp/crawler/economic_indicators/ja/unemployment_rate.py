from ..fred import FredCrawler


class UnemploymentRateCrawler(FredCrawler):

    def _get_tag(self):
        return 'LRUN64TTJPM156S'

    def _get_name(self):
        return 'unemployment_rate'
