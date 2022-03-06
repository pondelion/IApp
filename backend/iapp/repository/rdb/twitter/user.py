from typing import List, Optional

from ..base import BaseRDBRepository
from ....db.rdb import Session
from ....models.sqlalchemy.twitter import TwitterUser as TwitterUserModel
from ....schemas.twitter import TwitterUser as TwitterUserSchema


class TwitterUserRepository(BaseRDBRepository[TwitterUserModel, TwitterUserSchema, TwitterUserSchema]):

    def __init__(self):
        super().__init__(TwitterUserModel)

    def get_by_screen_name(self, db: Session, *, screen_name: str) -> Optional[TwitterUserModel]:
        return db.query(TwitterUserModel).filter(TwitterUserModel.screen_name == screen_name).first()
