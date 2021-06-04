from typing import List, Union, Optional

from overrides import overrides

from ..repository import Repository
from ...storage import Storage, StorageType
from ...db import DB, DBType
from ...entity.twitter import (
    TwitterTweet,
)
from ...crawler.twitter.tweepy_crawler import (
    UserTweetCrawler
)
from ...crawler.callback import Callback, DefaultCallback


class TweetRepository(Repository):

    def __init__(
        self,
        storage: Storage = None,
        db: DB = None,
        media_storage: Storage = None,
    ):
        super().__init__(storage, db)
        self._media_storage = media_storage

    def _save_storage(
        self, data: Union[Tweet, List[Tweet]],
        filepath: str
    ) -> None:
        raise NotImplementedError("""
            Storage saving is not supported for tweet data.
        """)

    def _save_db(self, data: Union[Tweet, List[Tweet]]) -> None:
        if not isinstance(data, list):
            data = [data]
        json_data = [d.json() for d in data]
        self.db.save(json_data)

    def find(
        self,
        screen_name: str,
        callback: Callback = DefaultCallback()
    ) -> Optional[List[TwitterTweet]]:
        if self._db is not None:
            # fetching the data from DB.
            if self._db.type == DBType.DYNAMO_DB:
                twitter_tweets = self._find_from_dynamodb(
                    screen_name,
                    self._db
                )
            else:
                raise NotImplementedError()
            if twitter_user is not None and not self._need_update(twitter_user):
                # return the data stored in db.
                return twitter_user
            # the data in db is old, updating data with twitter API.
            twitter_user = self._crawler.crawl(screen_name=screen_name)
            if twitter_user is not None:
                self._save_db(twitter_user)
            return twitter_user
        else:
            return self._crawler.crawl(screen_name=screen_name)

    @overrides
    def _supported_storage_types(self) -> List[StorageType]:
        return []

    @overrides
    def _supported_db_types(self) -> List[DBType]:
        return []