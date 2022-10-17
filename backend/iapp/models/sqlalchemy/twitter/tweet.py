from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String)
from sqlalchemy.dialects.mysql import DATETIME, TEXT
from sqlalchemy.sql.functions import current_timestamp

from ..base import Base


class TwitterTweet(Base):
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    tweet_created_at = Column(DateTime(timezone=True), nullable=False)
    text = Column(TEXT, nullable=False)
    retweet_count = Column(Integer, nullable=False)
    favorite_count = Column(Integer, nullable=False)
    lang = Column(TEXT, nullable=True)
    user_id = Column(BigInteger, ForeignKey("twitteruser.id", ondelete='CASCADE'), nullable=False)
    has_media_files = Column(Boolean, nullable=False)
    # media_file_id = Column(BigInteger, ForeignKey("twittermediafile.id"), nullable=True)
    in_reply_to_user_id = Column(BigInteger, nullable=True)
    in_reply_to_screen_name = Column(TEXT, nullable=True)
    created_at = Column(
        DATETIME(fsp=6, timezone=True),
        server_default=current_timestamp(6).op('AT TIME ZONE')('UTC')
    )
    updated_at = Column(
        DATETIME(fsp=6, timezone=True),
        server_default=current_timestamp(6).op('AT TIME ZONE')('UTC'),
        onupdate=current_timestamp(6).op('AT TIME ZONE')('UTC')
    )
