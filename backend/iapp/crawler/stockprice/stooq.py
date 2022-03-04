from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas_datareader.data as web

from ..base_crawler import BaseCrawler


class StooqCrawler(BaseCrawler):

    def run(
        self,
        code: int,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
        start: datetime=datetime.now()-relativedelta(years=50),
        end: datetime=datetime.now()
    ) -> None:
        kwargs = {'code': code}

        try:
            df = web.DataReader(
                f'{code}.JP', 'stooq',
                start=start,
                end=end
            )
            if len(df) < 10:
                raise Exception('data length too short.')
            callback.on_finished(df, kwargs)
        except Exception as e:
            callback.on_failed(e, kwargs)

    def check_restriction(self):
        try:
            df = web.DataReader(
                '7203.JP', 'stooq',
            )
            if len(df) == 0:
                return False
        except Exception:
            return False
        
        return True
