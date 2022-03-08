import os
from datetime import datetime
import time

import urllib
import pandas as pd

from iapp.crawler import TwitterUserCrawler
from iapp.db.dynamodb import DynamoDB
from iapp.storage.s3 import S3
from iapp.utils.config import AWSConfig, DataLocationConfig
from iapp.utils.dynamodb import format_data
from iapp.utils.logger import Logger
from iapp.schemas.twitter import TwitterUser as TwitterUserScheme
from iapp.models.sqlalchemy.twitter import TwitterUser as TwitterUserModel
from iapp.repository.rdb import (TwitterUserRepository)
from iapp.service.twitter import TwitterUserService
from iapp.db.rdb import db, init_rdb


TAG = 'twitter_user_crawl'
tus = TwitterUserService()


def main():
    #init_rdb(recreate_table=True)
    init_rdb()

    screen_name = 'TwitterJP'

    user = tus.get_user_by_screen_name(screen_name=screen_name)
    print(user)


if __name__ == '__main__':
    main()
