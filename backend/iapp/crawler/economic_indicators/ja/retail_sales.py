from ..fred import FredCrawler


class RetailSalesCrawler(FredCrawler):

    def _get_tag(self):
        return 'JPNSARTMISMEI'

    def _get_name(self):
        return 'retail_sales'
