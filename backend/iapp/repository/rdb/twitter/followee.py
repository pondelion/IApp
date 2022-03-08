from typing import List, Optional

from ..base import BaseRDBRepository
from ....db.rdb import Session
from ....models.sqlalchemy.twitter import TwitterFollowee as TwitterFolloweeModel
from ....schemas.twitter import TwitterFolloweeInDB as TwitterFolloweeSchema


class TwitterFolloweeRepository(BaseRDBRepository[TwitterFolloweeModel, TwitterFolloweeSchema, TwitterFolloweeSchema]):

    def __init__(self):
        super().__init__(TwitterFolloweeModel)

    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[List[TwitterFolloweeModel]]:
        return db.query(TwitterFolloweeModel).filter(TwitterFolloweeModel.user_id == user_id).all()

    def create_all(
        self,
        db: Session,
        *,
        data_list: List[TwitterFolloweeSchema],
        commit: bool = True,
    ) -> List[TwitterFolloweeModel]:
        filter_conditions_list = [
            [TwitterFolloweeModel.user_id==data.user_id, TwitterFolloweeModel.followee_id==data.followee_id] for data in data_list
        ]
        return super().create_all(
            db,
            data_list=data_list,
            commit=commit,
            check_already_exists_filter_conditions_list=filter_conditions_list
        )
