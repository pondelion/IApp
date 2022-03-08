from sqlalchemy import Boolean, BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import DATETIME, TEXT
from sqlalchemy.sql.functions import current_timestamp

from ..base import Base


class TwitterFollower(Base):
    id = Column(BigInteger, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey("twitteruser.id"), primary_key=True, nullable=False, index=True)
    follower_id = Column(BigInteger, ForeignKey("twitteruser.id"), primary_key=True, nullable=False, index=True)
    created_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6)
    )
    updated_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6),
        onupdate=current_timestamp(6)
    )
