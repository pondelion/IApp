from sqlalchemy import Boolean, BigInteger, Column, DateTime, ForeignKey, Integer, String, BigInteger
from sqlalchemy.dialects.mysql import DATETIME, TEXT
from sqlalchemy.sql.functions import current_timestamp

from ..base import Base


class TwitterMediaFile(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    tweet_id = Column(BigInteger, ForeignKey("twittertweet.id", ondelete='SET NULL'), nullable=True)
    user_id = Column(BigInteger, ForeignKey("twitteruser.id", ondelete='SET NULL'), nullable=True)
    media_url = Column(TEXT, nullable=False)
    media_s3_url = Column(TEXT)
    media_type = Column(TEXT, nullable=False)
    created_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6)
    )
    updated_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6),
        onupdate=current_timestamp(6)
    )
