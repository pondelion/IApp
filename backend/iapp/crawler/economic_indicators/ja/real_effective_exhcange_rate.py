from ..fred import FredCrawler


class RealEffectiveExchangeRateCrawler(FredCrawler):
    """Real effective exchange rates are calculated as weighted averages of
    bilateral exchange rates adjusted by relative consumer prices.
    """

    def _get_tag(self):
        return 'RBJPBIS'

    def _get_name(self):
        return 'real_effective_exchange_rate'
