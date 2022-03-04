from typing import List, Optional

from ..base import BaseRDBRepository
from ....db.rdb import Session
from ....models.sqlalchemy.twitter import TwitterTweet as TwitterTweetModel
from ....schemas.twitter import TwitterTweetInDB as TwitterTweetSchema


class TwitterTweetRepository(BaseRDBRepository[TwitterTweetModel, TwitterTweetSchema, TwitterTweetSchema]):

    def __init__(self):
        super().__init__(TwitterTweetModel)

    def get_by_user_id(self, db: Session, user_id: int) -> Optional[List[TwitterTweetModel]]:
        return db.query(TwitterTweetModel).filter(TwitterTweetModel.user_id == user_id).all()
