from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TwitterMedia(BaseModel):
    id: int
    tweet_id: int
    user_id: int
    media_url: str
    media_s3_url: str
    media_type: str


class TwitterMediaInDB(TwitterMedia):
    pass
