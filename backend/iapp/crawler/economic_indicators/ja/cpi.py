from ..fred import FredCrawler


class CPICrawler(FredCrawler):
    """消費者物価指数"""

    def _get_tag(self):
        return 'JPNCPIALLMINMEI'

    def _get_name(self):
        return 'cpi'
