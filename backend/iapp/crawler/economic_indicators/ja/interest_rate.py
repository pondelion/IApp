from ..fred import FredCrawler


class InterestRateCrawler(FredCrawler):

    def _get_tag(self):
        return 'INTDSRJPM193N'

    def _get_name(self):
        return 'interest_rate'
