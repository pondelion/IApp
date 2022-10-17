import math
import os
import urllib
from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

import pandas as pd
from tqdm import tqdm

from ...crawler import TwitterUserTweetCrawler
from ...db.rdb import db
from ...models.sqlalchemy.twitter import TwitterTweet as TwitterTweetModel
from ...models.sqlalchemy.twitter import TwitterUser as TwitterUserModel
from ...repository.rdb import (TwitterMediaRepository, TwitterTweetRepository,
                               TwitterUserRepository)
from ...schemas.twitter import TwitterMediaInDB as TwitterMediaSchema
from ...schemas.twitter import TwitterTweetInDB as TwitterTweetInDBSchema
from ...schemas.twitter import TwitterTweetInDB as TwitterTweetSchema
from ...schemas.twitter import TwitterUser as TwitterUserSchema
from ...schemas.twitter import TwitterUserInDB as TwitterUserInDBSchema
from ...settings import settings
from ...storage.s3 import S3
from ...utils.config import AWSConfig, DataLocationConfig
from ...utils.dynamodb import format_data
from ...utils.logger import Logger
from .twitter_user_service import TwitterUserService


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
        count: int = 200,
        count_per_page: int = 200,
        return_df: bool = False,
    ) -> Optional[Union[List[TwitterTweetSchema], pd.DataFrame]]:
        raise NotImplementedError

    @abstractmethod
    def get_tweet_by_screen_name(
        self,
        screen_name: str,
        *,
        force_crawl: bool = False,
        count: int = 200,
        count_per_page: int = 200,
        return_df: bool = False,
    ) -> Optional[Union[List[TwitterTweetSchema], pd.DataFrame]]:
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
        count: int = 200,
        count_per_page: int = 200,
        crawl_all_historical_tweets: bool = False,
        return_df: bool = False,
    ) -> Optional[Union[List[TwitterTweetSchema], pd.DataFrame]]:
        tweets = self._svc.get_tweet_by_user_id(
            id=id, force_crawl=force_crawl, count=count, count_per_page=count_per_page,
            crawl_all_historical_tweets=crawl_all_historical_tweets,
        )
        if return_df and tweets:
            tweets = pd.DataFrame([t.dict() for t in tweets])
        return tweets

    def get_tweet_by_screen_name(
        self,
        screen_name: str,
        *,
        force_crawl: bool = False,
        count: int = 200,
        count_per_page: int = 200,
        crawl_all_historical_tweets: bool = False,
        return_df: bool = False,
    ) -> Optional[Union[List[TwitterTweetSchema], pd.DataFrame]]:
        tweets = self._svc.get_tweet_by_screen_name(
            screen_name=screen_name, force_crawl=force_crawl, count=count, count_per_page=count_per_page,
            crawl_all_historical_tweets=crawl_all_historical_tweets,
        )
        if return_df and tweets:
            tweets = pd.DataFrame([t.dict() for t in tweets])
        return tweets


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
        count: int = 200,
        count_per_page: int = 200,
        # n_pages: int = 3,
        crawl_all_historical_tweets: bool = False,
    ) -> Optional[List[TwitterTweetInDBSchema]]:
        # get user data from db or crawl before getting tweets.
        target_user = self._tus.get_user(id=id)
        if target_user is None:
            Logger.w(self.__class__.__name__, f'User with id {id} not found')
            return []
        return self.get_tweet_by_user(
            user=target_user, force_crawl=force_crawl, count=count, count_per_page=count_per_page,
            crawl_all_historical_tweets=crawl_all_historical_tweets,
        )

    def get_tweet_by_screen_name(
        self,
        screen_name: str,
        *,
        force_crawl: bool = False,
        count: int = 200,
        count_per_page: int = 200,
        # n_pages: int = 3,
        crawl_since_last_tweet: bool = True,
        crawl_all_historical_tweets: bool = False,
    ) -> Optional[List[TwitterTweetInDBSchema]]:
        # get user data from db or crawl before getting tweets.
        target_user = self._tus.get_user_by_screen_name(screen_name=screen_name)
        if target_user is None:
            Logger.w(self.__class__.__name__, f'User {screen_name} not found')
            return []
        return self.get_tweet_by_user(
            user=target_user,
            force_crawl=force_crawl,
            count=count,
            count_per_page=count_per_page,
            crawl_since_last_tweet=crawl_since_last_tweet,
            crawl_all_historical_tweets=crawl_all_historical_tweets,
        )

    def get_tweet_by_user(
        self,
        user: TwitterUserInDBSchema,
        force_crawl: bool,
        count: int,
        count_per_page: int,
        # n_pages: int,
        crawl_since_last_tweet: Optional[bool] = True,
        crawl_all_historical_tweets: bool = False,
    ) -> Optional[List[TwitterTweetInDBSchema]]:
        latest_tweet = self._ttr.get_latest_tweet(self._db, user_id=user.id)
        latest_tweet_updated_at = latest_tweet.updated_at if latest_tweet else None
        latest_crawled_at = user.last_tweet_crawled_at
        print(f'latest_tweet_updated_at : {latest_tweet_updated_at}')
        if crawl_all_historical_tweets and user.histrical_crawled_at is None:
            count_per_page = 200  #
            count = 10000  # possible max count
            tweets = self._crawl_tweets(
                user=user, count=count, count_per_page=count_per_page, crawl_since_last_tweet=False,
                crawl_all_historical_tweets=crawl_all_historical_tweets
            )
            return tweets
        elif latest_crawled_at:
            # Tweets found in db for target user.
            ts = datetime.now()
            # elapsed_sec_since_last_update = (ts - latest_tweet_updated_at).total_seconds()
            elapsed_sec_since_last_update = (ts - latest_crawled_at).total_seconds()
            print(elapsed_sec_since_last_update)
            if force_crawl or (elapsed_sec_since_last_update > _TwitterTweetServiceMySQL.DEFAULT_DB_RECORD_REFRESH_SECS):
                # Over DEFAULT_DB_RECORD_REFRESH_SECS sec passed since last tweet updated, crawling new tweets and updating.
                print(f'Over {_TwitterTweetServiceMySQL.DEFAULT_DB_RECORD_REFRESH_SECS} sec passed since last crawl, crawling new tweets and updating.')
                tweets = self._crawl_tweets(
                    user=user, count=count, count_per_page=count_per_page, crawl_since_last_tweet=crawl_since_last_tweet,
                    crawl_all_historical_tweets=crawl_all_historical_tweets,
                )
                # return tweets
                return self._get_tweets_from_db(self._db, user, count=count)
            else:
                # Using tweets data in db as cache.
                print('Tweets data found in db, using cached data.')
                return self._get_tweets_from_db(self._db, user, count=count)
        else:
            # No tweets found in db for target user.
            print(f'tweets not found for user {user.screen_name}, crawling.')
            tweets = self._crawl_tweets(
                user=user, count=count, count_per_page=count_per_page, crawl_since_last_tweet=crawl_since_last_tweet,
                crawl_all_historical_tweets=crawl_all_historical_tweets,
            )
            return tweets

    def _crawl_tweets(
        self,
        user: TwitterUserInDBSchema,
        count: int,
        count_per_page: int,
        # n_pages: int,
        *,
        save_media_file: Optional[bool] = True,
        crawl_since_last_tweet: Optional[bool] = True,
        crawl_all_historical_tweets: bool = False,
    ) -> Optional[List[TwitterTweetInDBSchema]]:
        n_pages = math.ceil(count / min(count, count_per_page))
        kwargs = {
            'screen_name': user.screen_name,
            'count_per_page': count_per_page,
            'n_pages': n_pages
        }
        if user.last_tweet_id and crawl_since_last_tweet:
            kwargs['since_id'] = user.last_tweet_id
        dt_crawl = datetime.now()
        tweets, kwargs = self._utc.run(**kwargs)
        tweets = [format_data(tweet._json) for tweet in tweets]
        [tweet.update({'screen_name': user.screen_name}) for tweet in tweets]
        [tweet.update({'tweet_created_at': pd.to_datetime(tweet['created_at'])}) for tweet in tweets]
        # タイムゾーン有りだとDB保存時JSTへ自動変換後タイムゾーン情報が落ちてしまうのでタイムゾーン情報を消してJSTへ変換させない場合
        # [tweet.update({'tweet_created_at': pd.to_datetime(tweet['created_at']).replace(tzinfo=None)}) for tweet in tweets]
        [tweet.update({'user_id': tweet['user']['id']}) for tweet in tweets]
        [tweet.update({'has_media_files': True if 'media' in tweet['entities'] else False}) for tweet in tweets]
        ttss = [TwitterTweetSchema.parse_obj(tweet) for tweet in tweets]
        self._ttr.create_all(db, data_list=ttss, check_already_id_exists=True)
        Logger.d(self.__class__.__name__, f'Saved {len(ttss)} tweet data to RDB.')

        # Save media files
        for tweet in tqdm(tweets):
            if 'media' not in tweet['entities']:
                continue
            tweet_id = tweet['id']
            user_id = tweet['user']['id']
            medias = tweet['entities']['media']
            # s3_media_urls = []
            for media in medias:
                try:
                    media_id = media['id']
                    media_type = media['type']
                    media_url = media['media_url']
                    filename = media_url.split("/")[-1]
                    s3_filepath = None
                    if save_media_file:
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
                        # s3_media_urls.append(s3_filepath)
                    tms = TwitterMediaSchema(
                        id=media_id,
                        tweet_id=tweet_id,
                        user_id=user_id,
                        media_url=media_url,
                        media_s3_url=s3_filepath,
                        media_type=media_type,
                    )
                    self._tmr.upsert(db, data=tms)
                    # tweet.update({'media_file_id': media_id})
                except Exception as e:
                    print(e)
                    raise e

        # Update user last_tweet_id
        user_id = user.id
        latest_tweet_id = self._ttr.get_latest_tweet(db, user_id=user_id).id
        print(f'latest_tweet_id : {latest_tweet_id}')
        target_user = self._tur.get_by_id(db, id=user_id)
        ud = {
            'last_tweet_id': latest_tweet_id,
            'last_tweet_crawled_at': dt_crawl,
        }
        if crawl_all_historical_tweets:
            ud['histrical_crawled_at'] = datetime.now()
        self._tur.update(
            db,
            db_data=target_user,
            update_data=ud,
        )

        return ttss

    def _get_tweets_from_db(
        self,
        db,
        user: TwitterUserInDBSchema,
        count: Optional[int] = None,
    ) -> Optional[List[TwitterTweetSchema]]:
        tweets = self._ttr.get_by_user_id(db, user_id=user.id, count=count)
        if tweets is None:
            return None
        ttss = [TwitterTweetSchema.parse_obj(tweet.__dict__) for tweet in tweets]
        return ttss


class _TwitterTweetServiceDynamoDB(ITwitterTweetService):

    def save_tweet(self, data: TwitterTweetSchema) -> Optional[TwitterTweetSchema]:
        raise NotImplementedError

    def get_tweet_by_user_id(
        self,
        id: int,
        *,
        force_crawl: bool = False,
        count: int = 200,
        count_per_page: int = 200,
        # n_pages: int = 3,
        crawl_all_historical_tweets: bool = False,
    ) -> Optional[List[TwitterTweetInDBSchema]]:
        raise NotImplementedError

    def get_tweet_by_screen_name(
        self,
        screen_name: str,
        *,
        force_crawl: bool = False,
        count: int = 200,
        count_per_page: int = 200,
        # n_pages: int = 3,
        crawl_all_historical_tweets: bool = False,
    ) -> Optional[List[TwitterTweetInDBSchema]]:
        raise NotImplementedError
