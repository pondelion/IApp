from ..fred import FredCrawler


class GovernmentDebtCrawler(FredCrawler):

    def _get_tag(self):
        return 'DEBTTLJPA188A'

    def _get_name(self):
        return 'central_government_debt'
