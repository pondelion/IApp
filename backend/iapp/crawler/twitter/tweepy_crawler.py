from overrides import overrides
from typing import Any, Dict, Union

from ..base_crawler import BaseCrawler
from ..callback import ProgressResponse
from .api import TWEEPY_API


class UserTweetCrawler(BaseCrawler):

    def _crawl(
        self,
        screen_name: str,
        count_per_page: int,
        n_pages: int,
    ) -> Any:
        kwargs = {
            'screen_name': screen_name
        }
        pages = range(1, n_pages+1)

        all_tweets = []
        for page in pages:
            kwargs['page'] = page
            try:
                tweets = TWEEPY_API.user_timeline(
                    screen_name=screen_name,
                    count=count_per_page,
                    page=page
                )
                prog_res = self._on_progressed(data=tweets, kwargs=kwargs)
                all_tweets += tweets
                if prog_res == ProgressResponse.STOP_CRAWLING:
                    break
            except Exception as e:
                self._on_failed(e, kwargs)
        return self._on_completed(data=all_tweets, kwargs=kwargs)
