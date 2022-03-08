from typing import List, Optional

from ..base import BaseRDBRepository
from ....db.rdb import Session
from ....models.sqlalchemy.twitter import TwitterFollower as TwitterFollowerModel
from ....schemas.twitter import TwitterFollowerInDB as TwitterFollowerSchema


class TwitterFollowerRepository(BaseRDBRepository[TwitterFollowerModel, TwitterFollowerSchema, TwitterFollowerSchema]):

    def __init__(self):
        super().__init__(TwitterFollowerModel)

    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[List[TwitterFollowerModel]]:
        return db.query(TwitterFollowerModel).filter(TwitterFollowerModel.user_id == user_id).all()

    def create_all(
        self,
        db: Session,
        *,
        data_list: List[TwitterFollowerSchema],
        commit: bool = True,
    ) -> List[TwitterFollowerModel]:
        filter_conditions_list = [
            [TwitterFollowerModel.user_id==data.user_id, TwitterFollowerModel.follower_id==data.follower_id] for data in data_list
        ]
        return super().create_all(
            db,
            data_list=data_list,
            commit=commit,
            check_already_exists_filter_conditions_list=filter_conditions_list
        )
