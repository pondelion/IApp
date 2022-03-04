from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from typing import Optional, Union, List

import yfinance
import pandas as pd

from ..base_crawler import BaseCrawler
from ...utils.logger import Logger


class YfinanceCrawler(BaseCrawler):

    def run(
        self,
        code: Union[int, List[int]],
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
        period='max',
        start_dt: Optional[date] = None,
        end_dt: Optional[date] = None,
        min_data_length: int = 10
    ) -> None:
        kwargs = {'code': code}

        try:
            history_kwargs = {}
            if start_dt is not None:
                history_kwargs['start'] = kwargs['start_dt'] = start_dt
            if end_dt is not None:
                history_kwargs['end'] =  kwargs['end_dt'] = end_dt + timedelta(days=1)
            if start_dt is None and end_dt is None:
                history_kwargs['period'] = period

            if not isinstance(code, list):
                ticker = yfinance.Ticker(f'{code}.T')
                df = ticker.history(**history_kwargs)
            else:
                code_strs = [f'{c}.T' for c in code]
                tickers = yfinance.Tickers(' '.join(code_strs))
                df = tickers.history(**history_kwargs)
                df = self._process_multiticker_df(df, code_strs)
            if len(df) < min_data_length:
                raise Exception('data length too short.')
            callback.on_finished(df, kwargs)
        except Exception as e:
            callback.on_failed(e, kwargs)

    def _process_multiticker_df(self, df, code_strs):
        dfs = []
        COLUMNS = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
        for code_str in code_strs:
            try:
                df_ = df[[(col, code_str) for col in COLUMNS]]
                df_.columns = COLUMNS
                df_['Code'] = code_str.replace('.T', '')
                dfs.append(df_)
            except Exception as e:
                Logger.w('YfinanceCrawler._process_multiticker_df', e)
        df = pd.concat(dfs)
        df.index = pd.to_datetime(df.index)
        return df
