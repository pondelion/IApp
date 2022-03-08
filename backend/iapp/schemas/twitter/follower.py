from typing import List
from datetime import datetime

from pydantic import BaseModel


class TwitterFollower(BaseModel):
    user_id: int
    follower_user_ids: List[int]
    timestamp: datetime


class TwitterFollowerCreate(BaseModel):
    user_id: int
    follower_id: int


class TwitterFollowerInDB(BaseModel):
    id: int
    user_id: int
    follower_id: int
    created_at: datetime
    updated_at: datetime
