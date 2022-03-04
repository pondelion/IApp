from ..fred import FredCrawler


class InternationalTradeExportsCrawler(FredCrawler):

    def _get_tag(self):
        return 'JPNXTEXVA01CXMLM'

    def _get_name(self):
        return 'international_trade_exports'


class InternationalTradeImportsCrawler(FredCrawler):

    def _get_tag(self):
        return 'JPNXTIMVA01CXMLM'

    def _get_name(self):
        return 'international_trade_imports'
