from urllib.parse import quote

import feedparser
from timeout_decorator import timeout

from ...base_crawler import BaseCrawler
from ....utils.logger import Logger


class KeywordRSSCrawler(BaseCrawler):

    def __init__(self):
        self._RSS_URL_FMT = 'https://news.google.com/news/rss/search/section/q/{KEYWORD}/{KEYWORD}?ned=jp&amp;hl=ja&amp;gl=JP'

    def run(
        self,
        keyword: str,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> None:
        """[summary]

        Args:
            keyword (str): [description]
            callback (BaseCrawler.Callback, optional): [description]. Defaults to BaseCrawler.DefaultCallback().
        """

        kwargs = {
            'keyword': keyword
        }

        keyword_encoded = quote(keyword)

        try:
            feed = self._fetch(self._RSS_URL_FMT.format(KEYWORD=keyword_encoded))
            entries = feed.entries
        except Exception as e:
            callback.on_failed(e, kwargs)
            return

        callback.on_finished(entries, kwargs)

    @timeout(60)
    def _fetch(self, url):
        return feedparser.parse(url)
