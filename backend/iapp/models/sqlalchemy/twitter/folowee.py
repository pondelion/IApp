from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String)
from sqlalchemy.dialects.mysql import DATETIME, TEXT
from sqlalchemy.sql.functions import current_timestamp

from ..base import Base


class TwitterFollowee(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey("twitteruser.id", ondelete='CASCADE'), nullable=False)
    followee_id = Column(BigInteger, ForeignKey("twitteruser.id", ondelete='CASCADE'), nullable=False)
    created_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6).op('AT TIME ZONE')('UTC')
    )
    updated_at = Column(
        DATETIME(fsp=6),
        server_default=current_timestamp(6).op('AT TIME ZONE')('UTC'),
        onupdate=current_timestamp(6).op('AT TIME ZONE')('UTC')
    )
