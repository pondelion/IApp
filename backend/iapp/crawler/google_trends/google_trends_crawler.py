from datetime import datetime

from timeout_decorator import timeout
import pandas as pd
from pytrends.request import TrendReq

from ..base_crawler import BaseCrawler
from ...utils.logger import Logger


class GoogleTrendsCrawler(BaseCrawler):

    def run(
        self,
        pn: str='japan',
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> None:
        now_dt = datetime.now()
        kwargs = {
            'datetime': now_dt
        }

        try:
            df_trends = self._fetch(pn)
        except Exception as e:
            callback.on_failed(e, kwargs)
            return

        callback.on_finished(df_trends, kwargs)

    @timeout(60)
    def _fetch(self, pn: str) -> pd.DataFrame:
        pytrend = TrendReq(hl='ja-jp', tz=540)
        return pytrend.trending_searches(pn=pn)
