from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String)
from sqlalchemy.dialects.mysql import DATETIME, TEXT
from sqlalchemy.sql.functions import current_timestamp

from ..base import Base


class TwitterUser(Base):
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=False, nullable=False)
    name = Column(TEXT, nullable=False)
    screen_name = Column(TEXT, nullable=False)
    account_created_at = Column(DateTime, nullable=False)
    profile_image_url = Column(TEXT, nullable=False)
    followers_count = Column(Integer, nullable=False)
    friends_count = Column(Integer, nullable=False)
    protected = Column(Boolean, nullable=False)
    geo_enabled = Column(Boolean, nullable=False)
    description = Column(TEXT, nullable=True)
    location = Column(TEXT, nullable=True)
    time_zone = Column(TEXT, nullable=True)
    lang = Column(TEXT, nullable=True)
    last_tweet_id = Column(BigInteger, nullable=True)
    last_tweet_crawled_at = Column(DATETIME, nullable=True)
    histrical_crawled_at = Column(DATETIME, nullable=True)
    created_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6).op('AT TIME ZONE')('UTC')
    )
    updated_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6).op('AT TIME ZONE')('UTC'),
        onupdate=current_timestamp(6).op('AT TIME ZONE')('UTC')
    )
