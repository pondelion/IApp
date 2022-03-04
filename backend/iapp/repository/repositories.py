from enum import Enum
from .rdb import (
    TwitterUserRepository,
    TwitterTweetRepository,
)


class TwitterUserRepositories(Enum):
    MYSQL = TwitterUserRepository