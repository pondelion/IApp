from sqlalchemy import Boolean, BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import DATETIME, TEXT
from sqlalchemy.sql.functions import current_timestamp

from ..base import Base


class TwitterFollower(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey("twitteruser.id"), nullable=False)
    follower_id = Column(BigInteger, ForeignKey("twitteruser.id"), nullable=False)
    created_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6)
    )
    updated_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6),
        onupdate=current_timestamp(6)
    )
