from datetime import datetime
from abc import abstractmethod

import pandas_datareader.data as web

from ..base_crawler import BaseCrawler


class FredCrawler(BaseCrawler):

    def run(
        self,
        start_dt: datetime,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> None:
        self._run(
            start_dt,
            self._get_tag(),
            callback
        )

    def _run(
        self,
        start_dt: datetime,
        tag: str,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> None:
        kwargs = {
            'tag': tag,
            'name': self._get_name(),
        }
        try:
            data = web.DataReader(tag, 'fred', start_dt)
            callback.on_finished(data, kwargs)
        except Exception as e:
            callback.on_failed(e, kwargs)

    @abstractmethod
    def _get_tag(self):
        raise NotImplementedError

    @abstractmethod
    def _get_name(self):
        raise NotImplementedError
