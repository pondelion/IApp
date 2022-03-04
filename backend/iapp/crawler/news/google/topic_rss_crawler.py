from enum import Enum

import feedparser
from timeout_decorator import timeout

from ...base_crawler import BaseCrawler
from ....utils.logger import Logger


class Topic(Enum):
    BUSSINESS = 'https://news.google.com/news/rss/headlines/section/topic/BUSINESS.ja_jp/%E3%83%93%E3%82%B8%E3%83%8D%E3%82%B9?ned=jp&hl=ja&gl=JP'
    POLICTICS = 'https://news.google.com/news/rss/headlines/section/topic/POLITICS.ja_jp/%E6%94%BF%E6%B2%BB?ned=jp&hl=ja&gl=JP'
    TECHNOLOGY = 'https://news.google.com/news/rss/headlines/section/topic/SCITECH.ja_jp/%E3%83%86%E3%82%AF%E3%83%8E%E3%83%AD%E3%82%B8%E3%83%BC?ned=jp&hl=ja&gl=JP'
    SPORTS = 'https://news.google.com/news/rss/headlines/section/topic/SPORTS.ja_jp/%E3%82%B9%E3%83%9D%E3%83%BC%E3%83%84?ned=jp&hl=ja&gl=JP'
    ENTERTAINMENT = 'https://news.google.com/news/rss/headlines/section/topic/ENTERTAINMENT.ja_jp/%E3%82%A8%E3%83%B3%E3%82%BF%E3%83%A1?ned=jp&hl=ja&gl=JP'
    WORLD = 'https://news.google.com/news/rss/headlines/section/topic/WORLD.ja_jp/%E5%9B%BD%E9%9A%9B?ned=jp&hl=ja&gl=JP'
    NATION = 'https://news.google.com/news/rss/headlines/section/topic/NATION.ja_jp/%E5%9B%BD%E5%86%85?ned=jp&hl=ja&gl=JP'


class TopicRSSCrawler(BaseCrawler):

    def run(
        self,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
        topic: Topic = Topic.BUSSINESS
    ) -> None:
        """[summary]
        
        Args:
            callback (BaseCrawler.Callback, optional): [description]. Defaults to BaseCrawler.DefaultCallback().
            topic (Topic, optional): [description]. Defaults to Topic.BUSSINESS.
        """

        kwargs = {
            'topic': str(topic).replace('Topic.', '')
        }

        try:
            feed = self._fetch(topic.value)
            entries = feed.entries
            if not self._validate_results(entries):
                raise Exception('Invalid data.')
        except Exception as e:
            callback.on_failed(e, kwargs)
            return

        callback.on_finished(entries, kwargs)

    @timeout(60)
    def _fetch(self, url):
        return feedparser.parse(url)

    def _validate_results(self, entries):
        return all(['published_parsed' in entry for entry in entries])
