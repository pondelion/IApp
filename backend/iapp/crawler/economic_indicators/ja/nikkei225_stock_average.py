from ..fred import FredCrawler


class Nikkei225StockAverageCrawler(FredCrawler):

    def _get_tag(self):
        return 'NIKKEI225'

    def _get_name(self):
        return 'nikkei225_stock_average'
