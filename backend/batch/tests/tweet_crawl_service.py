import os
import time
import urllib
from datetime import datetime

import pandas as pd
from iapp.crawler import TwitterUserCrawler
from iapp.db.dynamodb import DynamoDB
from iapp.db.rdb import db, init_rdb
from iapp.models.sqlalchemy.twitter import TwitterTweet as TwitterTweetModel
from iapp.repository.rdb import TwitterTweetRepository
from iapp.schemas.twitter import TwitterTweet as TwitterTweetSchema
from iapp.service.twitter import TwitterTweetService
from iapp.storage.s3 import S3
from iapp.utils.config import AWSConfig, DataLocationConfig
from iapp.utils.dynamodb import format_data
from iapp.utils.logger import Logger

tts = TwitterTweetService()


def main():
    #init_rdb(recreate_table=True)
    init_rdb()

    screen_name = 'TwitterJP'

    tweets = tts.get_tweet_by_screen_name(
        screen_name=screen_name,
        # count_per_page=10,
        # n_pages=3,
        # crawl_all_historical_tweets=True,
    )
    print(tweets)


if __name__ == '__main__':
    main()
