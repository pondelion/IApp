from typing import List
from datetime import datetime

from pydantic import BaseModel


class TwitterFollower(BaseModel):
    user_id: int
    follower_user_ids: List[int]
    timestamp: datetime
