from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String)
from sqlalchemy.dialects.mysql import DATETIME, TEXT
from sqlalchemy.sql.functions import current_timestamp

from ..base import Base


class TwitterFollower(Base):
    id = Column(BigInteger, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey("twitteruser.id", ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    follower_id = Column(BigInteger, ForeignKey("twitteruser.id", ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    created_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6).op('AT TIME ZONE')('UTC')
    )
    updated_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6).op('AT TIME ZONE')('UTC'),
        onupdate=current_timestamp(6).op('AT TIME ZONE')('UTC')
    )
