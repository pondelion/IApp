import multiprocessing
from abc import ABCMeta, abstractmethod
from multiprocessing import Process
from typing import Dict, Generator, List, Optional
from datetime import datetime

from ..base_crawler import BaseCrawler
from .api import TWEEPY_API
from ...utils.logger import Logger


class TwitterUserTweetCrawler(BaseCrawler):

    def run(
        self,
        screen_name: str,
        count_per_page: int = 200,
        n_pages: int = 20,
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
        since_id: Optional[int] = None,
    ) -> Generator:
        itr = self._crawl(
            screen_name, count_per_page, n_pages, callback, since_id
        )
        for tweets, kwargs in itr:
            yield tweets, kwargs

    def _crawl(
        self,
        screen_name: str,
        count_per_page: int,
        n_pages: int,
        callback: BaseCrawler.Callback,
        since_id: Optional[int] = None,
    ) -> Generator:
        kwargs = {
            'screen_name': screen_name,
            'count': count_per_page,
        }
        if since_id is not None:
            kwargs['since_id'] = since_id
        pages = range(1, n_pages+1)

        for page in pages:
            kwargs['page'] = page
            try:
                tweets = TWEEPY_API.user_timeline(**kwargs)
                if len(tweets) == 0:
                    Logger.i('TwitterUserTweetCrawler', f'0 tweet fetched from user_timeline API. {kwargs}')
                    break
                callback.on_finished(tweets, kwargs)
                yield tweets, kwargs
            except Exception as e:
                callback.on_failed(e, kwargs)
