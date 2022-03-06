from typing import List, Optional

from sqlalchemy.sql import func

from ..base import BaseRDBRepository
from ....db.rdb import Session
from ....models.sqlalchemy.twitter import TwitterTweet as TwitterTweetModel
from ....schemas.twitter import TwitterTweetInDB as TwitterTweetSchema


class TwitterTweetRepository(BaseRDBRepository[TwitterTweetModel, TwitterTweetSchema, TwitterTweetSchema]):

    def __init__(self):
        super().__init__(TwitterTweetModel)

    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[List[TwitterTweetModel]]:
        return db.query(TwitterTweetModel).filter(TwitterTweetModel.user_id == user_id).all()

    def get_latest_tweet(self, db: Session, *, user_id: int) -> Optional[int]:
        result = db.query(func.max(TwitterTweetModel.id).label("max_id")).filter(TwitterTweetModel.user_id == user_id).one()
        return result[0] if result else None
