from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String)
from sqlalchemy.dialects.mysql import DATETIME, TEXT
from sqlalchemy.sql.functions import current_timestamp

from ..base import Base


class TwitterMediaFile(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    tweet_id = Column(BigInteger, ForeignKey("twittertweet.id", ondelete='CASCADE'), nullable=True)
    user_id = Column(BigInteger, ForeignKey("twitteruser.id", ondelete='SET NULL'), nullable=True)
    media_url = Column(TEXT, nullable=False)
    media_s3_url = Column(TEXT, nullable=True)
    media_type = Column(TEXT, nullable=False)
    created_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6).op('AT TIME ZONE')('UTC')
    )
    updated_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6).op('AT TIME ZONE')('UTC'),
        onupdate=current_timestamp(6).op('AT TIME ZONE')('UTC')
    )
