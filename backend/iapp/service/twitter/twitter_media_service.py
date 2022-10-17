from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import List, Optional

from ...db.rdb import db
from ...repository.rdb import TwitterUserRepository
from ...repository.rdb.twitter.media import TwitterMediaRepository
from ...schemas.twitter import TwitterMediaInDB as TwitterMediaInDBSchema


class BackendRepository(Enum):
    MYSQL = 'mysql'
    DYNAMODB = 'dynamodb'


DEFAULT_BACKEND = BackendRepository.MYSQL


class ITwitterMediaService(metaclass=ABCMeta):

    @abstractmethod
    def get_by_user_id(self, id: int) -> Optional[List[TwitterMediaInDBSchema]]:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_name(self, user_name: str) -> Optional[List[TwitterMediaInDBSchema]]:
        raise NotImplementedError

    @abstractmethod
    def get_by_tweet_id(self, tweet_id: int) -> Optional[List[TwitterMediaInDBSchema]]:
        raise NotImplementedError


class TwitterMediaService(ITwitterMediaService):

    def __init__(self, repo: BackendRepository = DEFAULT_BACKEND):
        self._repo = repo
        if repo == BackendRepository.MYSQL:
            self._svc = _TwitterMediaServiceMySQL()
        elif repo == BackendRepository.DYNAMODB:
            self._svc = _TwitterMediaServiceDynamoDB()
        else:
            raise ValueError(f'{repo} not supported.')

    def get_by_user_id(self, id: int) -> Optional[List[TwitterMediaInDBSchema]]:
        return self._svc.get_by_user_id(id=id)

    def get_by_user_name(self, user_name: str) -> Optional[List[TwitterMediaInDBSchema]]:
        return self._svc.get_by_user_name(user_name=user_name)

    def get_by_tweet_id(self, tweet_id: int) -> Optional[List[TwitterMediaInDBSchema]]:
        return self._svc.get_by_tweet_id(tweet_id=tweet_id)


class _TwitterMediaServiceMySQL(ITwitterMediaService):

    def __init__(self):
        self._tur = TwitterUserRepository()
        self._tmr = TwitterMediaRepository()
        self._db = db

    def get_by_user_id(self, id: int) -> Optional[List[TwitterMediaInDBSchema]]:
        medias = self._tmr.get_by_user_id(self._db, user_id=id)
        return [TwitterMediaInDBSchema.parse_obj(d.__dict__) for d in medias] if medias else []

    def get_by_user_name(self, user_name: str) -> Optional[List[TwitterMediaInDBSchema]]:
        medias = self._tmr.get_by_user_name(self._db, user_name=user_name)
        # print(medias)
        return [TwitterMediaInDBSchema.parse_obj(d.__dict__) for d in medias] if medias else []

    def get_by_tweet_id(self, tweet_id: int) -> Optional[List[TwitterMediaInDBSchema]]:
        medias = self._tmr.get_by_tweet_id(self._db, tweet_id=tweet_id)
        return [TwitterMediaInDBSchema.parse_obj(d.__dict__) for d in medias] if medias else []


class _TwitterMediaServiceDynamoDB(ITwitterMediaService):

    def get_by_user_id(self, id: int) -> Optional[List[TwitterMediaInDBSchema]]:
        raise NotImplementedError

    def get_by_user_name(self, user_name: str) -> Optional[List[TwitterMediaInDBSchema]]:
        raise NotImplementedError

    def get_by_tweet_id(self, tweet_id: int) -> Optional[List[TwitterMediaInDBSchema]]:
        raise NotImplementedError
