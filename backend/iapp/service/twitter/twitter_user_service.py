from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from ...db.rdb import db
from ...repository.rdb import (
    TwitterUserRepository,
    TwitterFollowerRepository,
    TwitterFolloweeRepository,
)
from ...schemas.twitter import (
    TwitterUser as TwitterUserSchema,
    TwitterUserInDB as TwitterUserInDBSchema,
    TwitterFollower as TwitterFollowerSchema,
    TwitterFollowee as TwitterFolloweeSchema,
)
from ...models.sqlalchemy.twitter import (
    TwitterUser as TwitterUserModel,
)
from ...crawler import TwitterUserCrawler


class BackendRepository(Enum):
    MYSQL = 'mysql'
    DYNAMODB = 'dynamodb'


DEFAULT_BACKEND = BackendRepository.MYSQL


class ITwitterUserService(metaclass=ABCMeta):

    @abstractmethod
    def save_user(self, data: TwitterUserSchema) -> Optional[TwitterUserInDBSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, id: int) -> Optional[TwitterUserInDBSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_screen_name(self, screen_name: str) -> Optional[TwitterUserInDBSchema]:
        raise NotImplementedError

    @abstractmethod
    def get_followers(self, id: int) -> Optional[List[TwitterUserInDBSchema]]:
        raise NotImplementedError

    @abstractmethod
    def get_followees(self, id: int) -> Optional[List[TwitterUserInDBSchema]]:
        raise NotImplementedError


class TwitterUserService(ITwitterUserService):

    def __init__(self, repo: BackendRepository = DEFAULT_BACKEND):
        self._repo = repo
        if repo == BackendRepository.MYSQL:
            self._svc = _TwitterUserServiceMySQL()
        elif repo == BackendRepository.DYNAMODB:
            self._svc = _TwitterUserServiceDynamoDB()
        else:
            raise ValueError(f'{repo} not supported.')

    def save_user(self, data: TwitterUserSchema) -> Optional[TwitterUserInDBSchema]:
        return self._svc.save_user(data=data)

    def get_user(self, id: int) -> Optional[TwitterUserInDBSchema]:
        return self._svc.get_user(id=id)

    def get_user_by_screen_name(self, screen_name: str) -> Optional[TwitterUserInDBSchema]:
        return self._svc.get_user_by_screen_name(screen_name=screen_name)

    def get_followers(self, id: int) -> Optional[List[TwitterUserInDBSchema]]:
        return self._svc.get_followers(id=id)

    def get_followees(self, id: int) -> Optional[List[TwitterUserInDBSchema]]:
        return self._svc.get_followees(id=id)


class _TwitterUserServiceMySQL(ITwitterUserService):

    DEFAULT_DB_RECORD_REFRESH_SECS = 60*60*24*3  # 3days

    def __init__(self):
        self._tur = TwitterUserRepository()
        self._db = db
        self._user_crawler = TwitterUserCrawler()
        self.DB_RECORD_REFRESH_SECS = _TwitterUserServiceMySQL.DEFAULT_DB_RECORD_REFRESH_SECS

    def save_user(self, data: TwitterUserSchema) -> Optional[TwitterUserInDBSchema]:
        target_user = self._tur.get_by_id(self._db, data.id)
        if target_user:
            # Alredy exists in db, updating.
            updated = self._tur.update_by_filter(
                self._db,
                filter_condition=TwitterUserModel.id == data.id,
                update_data=data
            )
            print(f'updated record : {updated}')
        else:
            # User doe's not exists in db, creating.
            self._tur.create(self._db, data=data)
            print(f'added new record : {data}')

    def get_user(self, id: int) -> Optional[TwitterUserInDBSchema]:
        user = self._tur.get_by_id(self._db, id)
        db_data = self._get_user_db_or_crawl(user, user_id_or_screen_name=id)
        return TwitterUserInDBSchema.parse_obj(db_data.__dict__)

    def get_user_by_screen_name(self, screen_name: str) -> Optional[TwitterUserInDBSchema]:
        user = self._tur.get_by_screen_name(self._db, screen_name=screen_name)
        db_data = self._get_user_db_or_crawl(user, user_id_or_screen_name=screen_name)
        return TwitterUserInDBSchema.parse_obj(db_data.__dict__)

    def _get_user_db_or_crawl(
        self,
        user: Optional[TwitterUserModel],
        user_id_or_screen_name: Union[int, str]
    ) -> TwitterUserModel:
        if user:
            # Alreay exists in db.
            print(f'twitter user [{user_id_or_screen_name}] already exists in db.')
            elapsed_since_last_update = (datetime.now() - user.updated_at).total_seconds()
            if elapsed_since_last_update > self.DB_RECORD_REFRESH_SECS:
                # The record is old, re-crawling
                print(f'{user_id_or_screen_name} : Over {self.DB_RECORD_REFRESH_SECS} secs past since last update, re-crawling')
                user_data = self._user_crawler.run(user_id_or_screen_name=user_id_or_screen_name)
                tus = TwitterUserSchema.parse_obj(user_data._json)
                updated = self._tur.update(
                    self._db,
                    db_data=user,
                    # filter_conditions=TwitterUserModel.screen_name==user_id_or_screen_name,
                    update_data=tus,
                )
                return updated
            else:
                print(f'{user_id_or_screen_name} : using data in db.')
                return user
        else:
            # The user does not exists in db, crawling.
            print(f'{user_id_or_screen_name} does not exists in db, crawling.')
            user_data = self._user_crawler.run(user_id_or_screen_name=user_id_or_screen_name)
            tus = TwitterUserSchema.parse_obj(user_data._json)
            created_user = self._tur.create(self._db, data=tus)
            return created_user

    def get_followers(self, id: int) -> Optional[List[TwitterUserInDBSchema]]:
        raise NotImplementedError

    def get_followees(self, id: int) -> Optional[List[TwitterUserInDBSchema]]:
        raise NotImplementedError


class _TwitterUserServiceDynamoDB(ITwitterUserService):

    def save_user(self, data: TwitterUserSchema) -> Optional[TwitterUserInDBSchema]:
        raise NotImplementedError

    def get_user(self, id: int) -> Optional[TwitterUserInDBSchema]:
        raise NotImplementedError

    def get_user_by_screen_name(self, screen_name: str) -> Optional[TwitterUserInDBSchema]:
        raise NotImplementedError

    def get_followers(self, id: int) -> Optional[List[TwitterUserInDBSchema]]:
        raise NotImplementedError

    def get_followees(self, id: int) -> Optional[List[TwitterUserInDBSchema]]:
        raise NotImplementedError
