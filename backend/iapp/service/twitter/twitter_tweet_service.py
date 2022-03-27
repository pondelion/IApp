from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
import os

import urllib
import pandas as pd

from ...db.rdb import db
from ...repository.rdb import (
    TwitterUserRepository,
    TwitterTweetRepository,
    TwitterMediaRepository,
)
from ...schemas.twitter import (
    TwitterUser as TwitterUserSchema,
    TwitterUserInDB as TwitterUserInDBSchema,
    TwitterTweetInDB as TwitterTweetInDBSchema,
    TwitterMediaInDB as TwitterMediaSchema,
    TwitterTweetInDB as TwitterTweetSchema,
)
from ...models.sqlalchemy.twitter import (
    TwitterUser as TwitterUserModel,
    TwitterTweet as TwitterTweetModel,
)
from ...crawler import (
    TwitterUserTweetCrawler,
    TwitterUserCrawler,
)
from .twitter_user_service import TwitterUserService
from ...storage.s3 import S3
from ...utils.config import AWSConfig, DataLocationConfig
from ...utils.dynamodb import format_data
from ...utils.logger import Logger
from ...settings import settings


class BackendRepository(Enum):
    MYSQL = 'mysql'
    DYNAMODB = 'dynamodb'


DEFAULT_BACKEND = BackendRepository.MYSQL


class ITwitterTweetService(metaclass=ABCMeta):

    @abstractmethod
    def save_tweet(self, data: TwitterTweetSchema) -> Optional[TwitterTweetSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_tweet_by_user_id(
        self,
        id: int,
        *,
        force_crawl: bool = False,
        count_per_page: int = 50,
        n_pages: int = 3,
    ) -> Optional[TwitterTweetSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_tweet_by_screen_name(
        self,
        screen_name: str,
        *,
        force_crawl: bool = False,
        count_per_page: int = 50,
        n_pages: int = 3,
    ) -> Optional[TwitterTweetSchema]:
        raise NotImplementedError


class TwitterTweetService(ITwitterTweetService):

    def __init__(self, repo: BackendRepository = DEFAULT_BACKEND):
        self._repo = repo
        if repo == BackendRepository.MYSQL:
            self._svc = _TwitterTweetServiceMySQL()
        elif repo == BackendRepository.DYNAMODB:
            self._svc = _TwitterTweetServiceDynamoDB()
        else:
            raise ValueError(f'{repo} not supported.')

    def save_tweet(self, data: TwitterTweetSchema) -> Optional[TwitterTweetSchema]:
        return self._svc.save_tweet(data=data)

    def get_tweet_by_user_id(
        self,
        id: int,
        *,
        force_crawl: bool = False,
        count_per_page: int = 50,
        n_pages: int = 3,
    ) -> Optional[TwitterTweetSchema]:
        return self._svc.get_tweet_by_user_id(
            id=id, force_crawl=force_crawl, count_per_page=count_per_page, n_pages=n_pages
        )

    def get_tweet_by_screen_name(
        self,
        screen_name: str,
        *,
        force_crawl: bool = False,
        count_per_page: int = 50,
        n_pages: int = 3,
    ) -> Optional[TwitterTweetSchema]:
        return self._svc.get_tweet_by_screen_name(
            screen_name=screen_name, force_crawl=force_crawl, count_per_page=count_per_page, n_pages=n_pages
        )


class _TwitterTweetServiceMySQL(ITwitterTweetService):

    DEFAULT_DB_RECORD_REFRESH_SECS = settings.DEFAULT_DB_RECORD_REFRESH_SECS

    def __init__(self):
        self._tus = TwitterUserService()
        self._db = db
        self._utc = TwitterUserTweetCrawler()
        self._tur = TwitterUserRepository()
        self._ttr = TwitterTweetRepository()
        self._tmr = TwitterMediaRepository()
        self._bucket = S3()

    def save_tweet(self, data: TwitterTweetSchema) -> Optional[TwitterTweetSchema]:
        raise NotImplementedError

    def get_tweet_by_user_id(
        self,
        id: int,
        *,
        force_crawl: bool = False,
        count_per_page: int = 50,
        n_pages: int = 3,
    ) -> Optional[TwitterTweetSchema]:
        # get user data from db or crawl before getting tweets.
        target_user = self._tus.get_user(id=id)
        return self.get_tweet_by_user(
            user=target_user, force_crawl=force_crawl, count_per_page=count_per_page, n_pages=n_pages
        )

    def get_tweet_by_screen_name(
        self,
        screen_name: str,
        *,
        force_crawl: bool = False,
        count_per_page: int = 50,
        n_pages: int = 3,
    ) -> Optional[TwitterTweetSchema]:
        # get user data from db or crawl before getting tweets.
        target_user = self._tus.get_user_by_screen_name(screen_name=screen_name)
        return self.get_tweet_by_user(
            user=target_user, force_crawl=force_crawl, count_per_page=count_per_page, n_pages=n_pages
        )

    def get_tweet_by_user(
        self,
        user: TwitterUserInDBSchema,
        force_crawl: bool,
        count_per_page: int,
        n_pages: int,
    ) -> Optional[List[TwitterTweetInDBSchema]]:
        latest_tweet_updated_at = None
        if latest_tweet_updated_at:
            # Tweets found in db for target user.
            ts = datetime.now()
            elapsed_sec_since_last_update = (ts - latest_tweet_updated_at).total_seconds()
            print(elapsed_sec_since_last_update)
            if force_crawl or (elapsed_sec_since_last_update > _TwitterTweetServiceMySQL.DEFAULT_DB_RECORD_REFRESH_SECS):
                # Over DEFAULT_DB_RECORD_REFRESH_SECS sec passed since last tweet updated, crawling new tweets and updating.
                print(f'Over {_TwitterTweetServiceMySQL.DEFAULT_DB_RECORD_REFRESH_SECS} sec passed since updated, crawling new tweets and updating.')
                tweets = self._crawl_tweets(user, count_per_page, n_pages)
                return tweets
            else:
                # Using tweets data in db as cache.
                print('Tweets data found in db, using cached data.')
                return self._get_tweets_from_db(user, count_per_page, n_pages)
        else:
            # No tweets found in db for target user.
            print(f'tweets not found for user {user.screen_name}, crawling.')
            tweets = self._crawl_tweets(user, count_per_page, n_pages)
            return tweets

    def _crawl_tweets(
        self,
        user: TwitterUserInDBSchema,
        count_per_page: int,
        n_pages: int,
    ) -> Optional[List[TwitterTweetInDBSchema]]:
        kwargs = {
            'screen_name': user.screen_name,
            'count_per_page': count_per_page,
            'n_pages': n_pages
        }
        if user.last_tweet_id:
            kwargs['since_id'] = user.last_tweet_id
        tweets, kwargs = self._utc.run(**kwargs)
        tweets = [format_data(tweet._json) for tweet in tweets]
        [tweet.update({'screen_name': user.screen_name}) for tweet in tweets]
        [tweet.update({'tweet_created_at': pd.to_datetime(tweet['created_at'])}) for tweet in tweets]
        [tweet.update({'user_id': tweet['user']['id']}) for tweet in tweets]
        [tweet.update({'has_media_files': True if 'media' in tweet['entities'] else False}) for tweet in tweets]
        ttss = [TwitterTweetSchema.parse_obj(tweet) for tweet in tweets]
        self._ttr.create_all(db, data_list=ttss, check_already_id_exists=True)

        # Save media files
        for tweet in tweets:
            if 'media' not in tweet['entities']:
                continue
            tweet_id = tweet['id']
            user_id = tweet['user']['id']
            medias = tweet['entities']['media']
            s3_media_urls = []
            for media in medias:
                try:
                    media_id = media['id']
                    media_type = media['type']
                    media_url = media['media_url']
                    filename = media_url.split("/")[-1]
                    local_tmp_filepath = f'/tmp/{filename}'
                    urllib.request.urlretrieve(media_url, local_tmp_filepath)
                    s3_filepath = os.path.join(
                        DataLocationConfig.TWITTER_MEDIAFILE_DIR,
                        f'{user_id}',
                        filename,
                    )
                    self._bucket.save(local_tmp_filepath, s3_filepath)
                    os.remove(local_tmp_filepath)
                    Logger.d(self.__class__.__name__, f'Saved media file to {s3_filepath}')
                    s3_media_urls.append(s3_filepath)
                    tms = TwitterMediaSchema(
                        id=media_id,
                        tweet_id=tweet_id,
                        user_id=user_id,
                        media_url=media_url,
                        media_s3_url=s3_filepath,
                        media_type=media_type,
                    )
                    self._tmr.upsert(db, data=tms)
                except Exception as e:
                    print(e)
                    raise e

        # Update user last_tweet_id
        user_id = user.id
        latest_tweet_id = self._ttr.get_latest_tweet(db, user_id=user_id)
        print(f'latest_tweet_id : {latest_tweet_id}')
        target_user = self._tur.get_by_id(db, id=user_id)
        self._tur.update(db, db_data=target_user, update_data={'last_tweet_id': latest_tweet_id})

        return ttss


class _TwitterTweetServiceDynamoDB(ITwitterTweetService):

    def save_tweet(self, data: TwitterTweetSchema) -> Optional[TwitterTweetSchema]:
        raise NotImplementedError

    def get_tweet_by_user_id(
        self,
        id: int,
        *,
        force_crawl: bool = False,
        count_per_page: int = 50,
        n_pages: int = 3,
    ) -> Optional[TwitterTweetSchema]:
        raise NotImplementedError

    def get_tweet_by_screen_name(
        self,
        screen_name: str,
        *,
        force_crawl: bool = False,
        count_per_page: int = 50,
        n_pages: int = 3,
    ) -> Optional[TwitterTweetSchema]:
        raise NotImplementedError
