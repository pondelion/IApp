from ..fred import FredCrawler


class IndustrialProductionCrawler(FredCrawler):

    def _get_tag(self):
        return 'JPNPROINDMISMEI'

    def _get_name(self):
        return 'industrial_production'
