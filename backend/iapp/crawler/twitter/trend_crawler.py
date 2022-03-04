from datetime import datetime

from timeout_decorator import timeout

from ..base_crawler import BaseCrawler
from .api import TWITTER_API
from ...utils.logger import Logger


class TwitterTrendCrawler(BaseCrawler):

    def __init__(
        self,
    ):
        self._TREND_URL = 'https://api.twitter.com/1.1/trends/place.json'

    def run(
        self,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
        id: int = 1118370
    ) -> None:
        params = {
            'id': id
        }
        try:
            ret = self._fetch(
                url=self._TREND_URL,
                params=params
            )
        except Exception as e:
            Logger.e('TrendCrawler#run', f'Failed to get from {self._TREND_URL} : {e}')
            callback.on_failed(e, {})
            return

        if ret.status_code != 200:
            Logger.e('TrendCrawler#run', 'status_code != 200')
            callback.on_failed(Exception('status_code != 200'), {})
            return

        dt_now = datetime.now()

        trends = [{
            'keyword': trend['name'],
            'volume': trend['tweet_volume'],
            'datetime': dt_now,
            'date': dt_now.date(),
        } for trend in ret.json()[0]['trends']]

        callback.on_finished(trends, {})

    @timeout(60)
    def _fetch(self, url, params):
        ret = TWITTER_API.get(
            url=self._TREND_URL,
            params=params
        )
        return ret
