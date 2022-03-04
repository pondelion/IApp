from ..fred import FredCrawler


class TotalIndustryProductionCrawler(FredCrawler):

    def _get_tag(self):
        return 'JPNPROINDMISMEI'

    def _get_name(self):
        return 'total_industry_production'
