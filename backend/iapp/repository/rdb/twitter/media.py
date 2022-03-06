from typing import List, Optional

from ..base import BaseRDBRepository
from ....db.rdb import Session
from ....models.sqlalchemy.twitter import TwitterMediaFile as TwitterMediaModel
from ....schemas.twitter import TwitterMediaInDB as TwitterMediaSchema


class TwitterMediaRepository(BaseRDBRepository[TwitterMediaModel, TwitterMediaSchema, TwitterMediaSchema]):

    def __init__(self):
        super().__init__(TwitterMediaModel)

    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[List[TwitterMediaModel]]:
        return db.query(TwitterMediaModel).filter(TwitterMediaModel.user_id == user_id).all()

    def get_by_tweet_id(self, db: Session, *, tweet_id: int) -> Optional[List[TwitterMediaModel]]:
        return db.query(TwitterMediaModel).filter(TwitterMediaModel.tweet_id == tweet_id).all()
