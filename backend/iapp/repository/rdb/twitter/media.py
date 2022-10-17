from typing import List, Optional

from ....db.rdb import Session
from ....models.sqlalchemy.twitter import TwitterMediaFile as TwitterMediaModel
from ....models.sqlalchemy.twitter import TwitterUser as TwitterUserModel
from ....schemas.twitter import TwitterMediaInDB as TwitterMediaSchema
from ..base import BaseRDBRepository


class TwitterMediaRepository(BaseRDBRepository[TwitterMediaModel, TwitterMediaSchema, TwitterMediaSchema]):

    def __init__(self):
        super().__init__(TwitterMediaModel)

    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[List[TwitterMediaModel]]:
        return db.query(TwitterMediaModel).filter(TwitterMediaModel.user_id == user_id).all()

    def get_by_user_name(self, db: Session, *, user_name: str) -> Optional[List[TwitterMediaModel]]:
        res = (
            db.query(
                TwitterMediaModel, TwitterUserModel
            ).join(
                TwitterMediaModel, TwitterMediaModel.user_id == TwitterUserModel.id
            ).filter(
                TwitterUserModel.screen_name == user_name
            ).all()
        )
        return [r[0] for r in res] if res else None

    def get_by_tweet_id(self, db: Session, *, tweet_id: int) -> Optional[List[TwitterMediaModel]]:
        return db.query(TwitterMediaModel).filter(TwitterMediaModel.tweet_id == tweet_id).all()
