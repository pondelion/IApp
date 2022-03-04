import multiprocessing
from abc import ABCMeta, abstractmethod
from multiprocessing import Process
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

import tweepy
import pandas as pd

from ..base_crawler import BaseCrawler
from .api import TWEEPY_API


class TwitterUserCrawler(BaseCrawler):

    def run(
        self,
        user_id_or_screen_name: Union[int, str],
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> Any:
        return self._crawl(
            user_id_or_screen_name, callback
        )

    def _crawl(
        self,
        user_id_or_screen_name: Union[int, str],
        callback: BaseCrawler.Callback,
    ) -> Any:
        kwargs = {
            'user_id_or_screen_name': user_id_or_screen_name,
        }

        try:
            user = TWEEPY_API.get_user(user_id_or_screen_name)
            user._json['account_created_at'] = str(pd.to_datetime(user._json['created_at']))
            callback.on_finished(user, kwargs)
            return user
        except Exception as e:
            callback.on_failed(e, kwargs)
            return None


class TwitterFollowerCrawler(BaseCrawler):

    def run(
        self,
        user_id_or_screen_name: Union[int, str],
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> Any:
        return self._crawl(
            user_id_or_screen_name, callback
        )

    def _crawl(
        self,
        user_id_or_screen_name: Union[int, str],
        callback: BaseCrawler.Callback,
    ) -> Any:
        kwargs = {
            'user_id_or_screen_name': user_id_or_screen_name,
        }

        try:
            c = tweepy.Cursor(TWEEPY_API.followers, user_id_or_screen_name)
            callback.on_finished(list(c.items()), kwargs)
            return list(c.items())
        except Exception as e:
            callback.on_failed(e, kwargs)
            return None


class TwitterFolloweeCrawler(BaseCrawler):

    def run(
        self,
        user_id_or_screen_name: Union[int, str],
        callback: BaseCrawler.Callback = BaseCrawler.DefaultCallback(),
    ) -> Any:
        return self._crawl(
            user_id_or_screen_name, callback
        )

    def _crawl(
        self,
        user_id_or_screen_name: Union[int, str],
        callback: BaseCrawler.Callback,
    ) -> Any:
        kwargs = {
            'user_id_or_screen_name': user_id_or_screen_name,
        }

        try:
            c = tweepy.Cursor(TWEEPY_API.friends, user_id_or_screen_name)
            callback.on_finished(list(c.items()), kwargs)
            return list(c.items())
        except Exception as e:
            callback.on_failed(e, kwargs)
            return None