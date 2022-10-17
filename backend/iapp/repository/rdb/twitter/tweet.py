from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.sql import func

from ....db.rdb import Session
from ....models.sqlalchemy.twitter import TwitterTweet as TwitterTweetModel
from ....schemas.twitter import TwitterTweetInDB as TwitterTweetSchema
from ..base import BaseRDBRepository


class TwitterTweetRepository(BaseRDBRepository[TwitterTweetModel, TwitterTweetSchema, TwitterTweetSchema]):

    def __init__(self):
        super().__init__(TwitterTweetModel)

    def get_by_user_id(self, db: Session, *, user_id: int, count: Optional[int] = None) -> Optional[List[TwitterTweetModel]]:
        qry = db.query(TwitterTweetModel).filter(TwitterTweetModel.user_id == user_id)
        if count is not None:
            qry = qry.order_by(desc(TwitterTweetModel.tweet_created_at)).limit(count)
        return qry.all()

    def get_latest_tweet(self, db: Session, *, user_id: int, count: Optional[int] = None) -> Optional[TwitterTweetModel]:
        subqry = db.query(
            func.max(TwitterTweetModel.id)
        ).filter(
            TwitterTweetModel.user_id == user_id
        ).scalar_subquery()
        result = db.query(TwitterTweetModel).filter(
            TwitterTweetModel.user_id == user_id,
            TwitterTweetModel.id == subqry,
        ).first()
        return result
