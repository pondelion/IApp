from datetime import datetime
from dateutil.relativedelta import relativedelta

import yfinance

from ..base_crawler import BaseCrawler


class FinancialsCrawler(BaseCrawler):

    def run(
        self,
        code: int,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> None:
        kwargs = {'code': code}

        try:
            ticker = yfinance.Ticker(f'{code}.T')
            df = ticker.financials
            if len(df) < 3:
                raise Exception('data length too short.')
            df = df.T
            df.index.name = 'Date'
            callback.on_finished(df, kwargs)
        except Exception as e:
            callback.on_failed(e, kwargs)


class BalanceSheetCrawler(BaseCrawler):

    def run(
        self,
        code: int,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> None:
        kwargs = {'code': code}

        try:
            ticker = yfinance.Ticker(f'{code}.T')
            df = ticker.balance_sheet
            if len(df) < 3:
                raise Exception('data length too short.')
            df = df.T
            df.index.name = 'Date'
            callback.on_finished(df, kwargs)
        except Exception as e:
            callback.on_failed(e, kwargs)


class CashflowCrawler(BaseCrawler):

    def run(
        self,
        code: int,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> None:
        kwargs = {'code': code}

        try:
            ticker = yfinance.Ticker(f'{code}.T')
            df = ticker.cashflow
            if len(df) < 3:
                raise Exception('data length too short.')
            df = df.T
            df.index.name = 'Date'
            callback.on_finished(df, kwargs)
        except Exception as e:
            callback.on_failed(e, kwargs)
