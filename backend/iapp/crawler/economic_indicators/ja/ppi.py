from ..fred import FredCrawler


class PPICrawler(FredCrawler):
    """生産者物価指数"""

    def _get_tag(self):
        return 'PITGCG01JPM661N'

    def _get_name(self):
        return 'ppi'
