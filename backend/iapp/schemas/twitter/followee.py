from typing import List
from datetime import datetime

from pydantic import BaseModel


class TwitterFollowee(BaseModel):
    user_id: int
    followee_user_ids: List[int]
    timestamp: datetime
