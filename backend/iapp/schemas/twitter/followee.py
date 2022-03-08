from typing import List
from datetime import datetime

from pydantic import BaseModel


class TwitterFollowee(BaseModel):
    user_id: int
    followee_user_ids: List[int]
    timestamp: datetime


class TwitterFolloweeCreate(BaseModel):
    user_id: int
    followee_id: int


class TwitterFolloweeInDB(BaseModel):
    id: int
    user_id: int
    followee_id: int
    created_at: datetime
    updated_at: datetime
