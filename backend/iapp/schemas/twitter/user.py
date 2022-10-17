from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TwitterUser(BaseModel):
    id: int
    name: str
    screen_name: str
    account_created_at: datetime
    profile_image_url: str
    followers_count: int
    friends_count: int
    protected: bool
    geo_enabled: bool
    description: Optional[str] = ''
    location: Optional[str] = ''
    time_zone: Optional[str] = None
    lang: Optional[str] = None


class TwitterUserInDB(TwitterUser):
    last_tweet_id: Optional[int] = None
    last_tweet_crawled_at: Optional[datetime] = None
    histrical_crawled_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
