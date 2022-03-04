from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional

from ...db.rdb import db
from ...repository.rdb import (
    TwitterUserRepository
)
from ...schemas.twitter import (
    TwitterUser as TwitterUserSchema,
    TwitterFollower as TwitterFollowerSchema,
    TwitterFollowee as TwitterFolloweeSchema,
)
from ...models.sqlalchemy.twitter import (
    TwitterUser as TwitterUserModel,
)



class BackendRepository(Enum):
    MYSQL
    DYNAMODB


class ITwitterUserService(metaclass=ABCMeta):

    @abstractmethod
    def save_user(self, data: TwitterUserSchema) -> Optional[TwitterUserSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, id: int) -> Optional[TwitterUserSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_screen_name(self, screen_name: str) -> Optional[TwitterUserSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_followers(self, id: int) -> Optional[List[TwitterUserSchema]]:
        raise NotImplementedError

    @abstractmethod
    def get_followees(self, id: int) -> Optional[List[TwitterUserSchema]]:
        raise NotImplementedError


class TwitterUserService(ITwitterUserService):

    def __init__(self, repo: BackendRepository = BackendRepository.MYSQL):
        self._repo = repo
        if repo == BackendRepository.MYSQL:
            self._svc = _TwitterUserServiceMySQL()
        elif repo == BackendRepository.DYNAMODB:
            self._svc = _TwitterUserServiceDynamoDB()
        else:
            raise ValueError(f'{repo} not supported.')

    def save_user(self, data: TwitterUserSchema) -> Optional[TwitterUserSchema]:
        return self._svc.save_user(data=data)

    def get_user(self, id: int) -> Optional[TwitterUserSchema]:
        return self._svc.get_user(id=id)

    def get_user_by_screen_name(self, screen_name: str) -> Optional[TwitterUserSchema]:
        return self._svc.get_user_by_screen_name(screen_name=screen_name)

    def get_followers(self, id: int) -> Optional[List[TwitterUserSchema]]:
        return self._svc.get_followers(id=id)

    def get_followees(self, id: int) -> Optional[List[TwitterUserSchema]]:
        return self._svc.get_followees(id=id)


class _TwitterUserServiceMySQL(ITwitterUserService):

    def __init__(self):
        self._tur = TwitterUserRepository()
        DB_RECORD_REFRESH_SECS = 60*60*24*3  # 3days

    def save_user(self, data: TwitterUserSchema) -> Optional[TwitterUserSchema]:
        target_user = self._tur.get_by_id(db, data.id)
        if target_user:
            # Alredy exists in db, updating.
            updated = self._tur.update_by_filter(
                db,
                filter_condition=TwitterUserModel.id == data.id,
                update_data=data
            )
            print(f'updated record : {updated}')
        else:
            # User doe's not exists in db, creating.
            self._tur.create(db, data=data)
            print(f'added new record : {data}')

    def get_user(self, id: int) -> Optional[TwitterUserSchema]:
        user = self._tur.get_by_id(db, id)
        return self._get_user_db_or_crawl(user)

    def get_user_by_screen_name(self, screen_name: str) -> Optional[TwitterUserSchema]:
        user = self._tur.get_by_screen_name(db, screen_name)
        return self._get_user_db_or_crawl(user)

    def _get_user_db_or_crawl(self, user: Optional[TwitterUserModel]):
        if user:
            # Alreay exists in db.
            elapsed_since_last_update = (datetime.now() - user.updated_at).total_seconds()
            if elapsed_since_last_update > self.DB_RECORD_REFRESH_SECS:
                # The record is old, re-crawling
                pass
            else:
                return user
        else:
            # The user does not exists in db, crawling.
            pass

class _TwitterUserServiceDynamoDB(ITwitterUserService):

    def save_user(self, data: TwitterUserSchema) -> Optional[TwitterUserSchema]:
        raise NotImplementedError

    def get_user(self, id: int) -> Optional[TwitterUserSchema]:
        raise NotImplementedError

    def get_user_by_screen_name(self, screen_name: str) -> Optional[TwitterUserSchema]:
        raise NotImplementedError

    def get_followers(self, id: int) -> Optional[List[TwitterUserSchema]]:
        raise NotImplementedError

    def get_followees(self, id: int) -> Optional[List[TwitterUserSchema]]:
        raise NotImplementedError