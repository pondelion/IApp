from typing import List, Union, Optional
from datetime import datetime, timedelta

from overrides import overrides

from ..repository import Repository
from ...storage import Storage, StorageType
from ...db import DB, DBType, DynamoDB
from ...entity.twitter import (
    TwitterUser,
)
from ...crawler.twitter.tweepy_crawler import (
    UserInfoCrawler
)
from ...utils.config import AWSConfig


class UserRepository(Repository):

    def __init__(
        self,
        storage: Storage = None,
        db: DB = DynamoDB(
            table_name=AWSConfig.DYNAMODB_TWITTER_USER_TABLE_NAME
        ),
    ):
        super().__init__(storage, db)
        self.DB_RECORD_UPDATE_PERIOD = timedelta(days=20)
        self._crawler = UserInfoCrawler()

    def _save_storage(
        self, data: Union[TwitterUser, List[TwitterUser]],
        filepath: str
    ) -> None:
        raise NotImplementedError("""
            Storage saving is not supported for tweet data.
        """)

    def _save_db(self, data: Union[TwitterUser, List[TwitterUser]]) -> None:
        if not isinstance(data, list):
            data = [data]
        json_data = [d.json() for d in data]
        self._db.save(json_data)

    def find(
        self,
        screen_name: str,
    ) -> Optional[TwitterUser]:
        if self._db is not None:
            # fetching the data from DB.
            if self._db.type == DBType.DYNAMO_DB:
                twitter_user = self._find_from_dynamodb(
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

    def _find_from_dynamodb(
        self,
        screen_name: str,
        dynamo_db: DynamoDB,
    ) -> TwitterUser:
        res = dynamo_db.partitionkey_query(
            partition_key_name='screen_name',
            partition_key=screen_name
        )
        twitter_user = TwitterUser.from_json(res)
        return twitter_user

    def _need_update(self, twitter_user: TwitterUser) -> bool:
        return twitter_user.updated_at < datetime.now() - self.DB_RECORD_UPDATE_PERIOD

    @overrides
    def _supported_storage_types(self) -> List[StorageType]:
        return []

    @overrides
    def _supported_db_types(self) -> List[DBType]:
        return [DBType.DYNAMO_DB]
