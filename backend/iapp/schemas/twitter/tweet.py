from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TwitterTweet(BaseModel):
    id: int
    tweet_created_at: datetime
    text: str
    retweet_count: int
    favorite_count: int
    lang: str
    user_id: int
    media_urls: Optional[List[str]] = []
    in_reply_to_user_id: Optional[int] = None
    in_reply_to_screen_name: Optional[str] = None


class TwitterTweetInDB(BaseModel):
    id: int
    tweet_created_at: datetime
    text: str
    retweet_count: int
    favorite_count: int
    lang: str
    user_id: int
    has_media_files: bool
    in_reply_to_user_id: Optional[int] = None
    in_reply_to_screen_name: Optional[str] = None
