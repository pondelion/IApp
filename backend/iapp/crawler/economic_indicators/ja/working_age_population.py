from ..fred import FredCrawler


class WorkingAgePopulationCrawler(FredCrawler):
    """生産年齢人口(15才-64才)
    """

    def _get_tag(self):
        return 'LFWA64TTJPM647S'

    def _get_name(self):
        return 'working_age_population'
