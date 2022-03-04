import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import time

import urllib
import pandas as pd

from iapp.crawler import TwitterUserTweetCrawler
from iapp.db.dynamodb import DynamoDB
from iapp.storage.s3 import S3
from iapp.utils.config import AWSConfig, DataLocationConfig
from iapp.utils.dynamodb import format_data
from iapp.utils.logger import Logger
from iapp.schemas.twitter import TwitterTweetInDB as TwitterTweetSchema
from iapp.models.sqlalchemy.twitter import TwitterTweet as TwitterTweetModel
from iapp.repository.rdb import (
    TwitterTweetRepository,
    TwitterUserRepository,
)
from iapp.db.rdb import db, init_rdb


TAG = 'twitter_tweet_crawl'
tur = TwitterUserRepository()
ttr = TwitterTweetRepository()


class Callback(TwitterUserTweetCrawler.Callback):

    def on_finished(self, data, args):
        Logger.d(TAG, 'on_finished')
        print(args)
        print(f'len(data) : {len(data)}')

        items = [format_data(item._json) for item in data]
        # print(items[:1])
        [item.update({'screen_name': args["screen_name"]}) for item in items]
        [item.update({'tweet_created_at': pd.to_datetime(item['created_at'])}) for item in items]
        [item.update({'user_id': item['user']['id']}) for item in items]
        [item.update({'has_media_files': True if 'media' in item['entities'] else False}) for item in items]
        ttss = [TwitterTweetSchema.parse_obj(item) for item in items]
        for tts in ttss:
            print(tts.dict())
            data = ttr.create(db, data=tts)
            print(f'saved')
        # for item, d in zip(items, data):
        #     item['created_at'] = int(d.created_at.timestamp())
        #     item['id'] = d.id
        #     if 'media' in item['entities']:
        #         try:
        #             s3_media_urls = []
        #             medias = item['entities']['media']
        #             for media in medias:
        #                 media_url = media['media_url']
        #                 filename = media_url.split("/")[-1]
        #                 local_tmp_filepath = f'/tmp/{filename}'
        #                 urllib.request.urlretrieve(
        #                     media_url,
        #                     local_tmp_filepath
        #                 )
        #                 s3_filepath = os.path.join(
        #                     DataLocationConfig.TWITTER_MEDIAFILE_DIR,
        #                     args["screen_name"],
        #                     filename
        #                 )
        #                 S3.save_file(local_tmp_filepath, s3_filepath, 'i-app')
        #                 os.remove(local_tmp_filepath)
        #                 Logger.d(TAG, f'Uploaded media file to {s3_filepath}')
        #                 s3_media_urls.append(s3_filepath)
        #             item['s3_media_urls'] = s3_media_urls
        #         except Exception as e:
        #             print(e)

        # DynamoDB.put_items(
        #     AWSConfig.DYNAMODB_TWITTER_USER_TWEET_TABLE_NAME,
        #     items,
        # )

    def on_failed(self, e, args):
        Logger.e(TAG, f'on_failed : {e} : {args}')


def main():
    # init_rdb(recreate_table=True)
    utc = TwitterUserTweetCrawler()

    screen_name = 'TwitterJP'

    ts1 = datetime.now()
    target_user = tur.get_by_screen_name(db, screen_name)
    target_tweets = ttr.get_by_user_id(db, target_user.id)
    print(f'target_user : {target_user.__dict__}')
    print(f'tweets : {target_tweets}')
    ts2 = datetime.now()
    print((ts2-ts1).total_seconds())
    if target_user.last_tweet_id:
        ts3 = datetime.now()
        elapsed_sec_since_last_update = (ts3-target_user.updated_at).total_seconds()
        print(elapsed_sec_since_last_update)
        if elapsed_sec_since_last_update > 60:
            print('Over 60 sec passed since updated. Re-crawling.')
            itr = utc.run(
                screen_name=screen_name,
                count_per_page=10,
                n_pages=2,
                callback=Callback(),
                since_id=target_user.last_tweet_id,
            )
            for tweets, kwargs in itr:
                print(f'{len(tweets)} :: ')
    else:
        print('No tweets record found')
        itr = utc.run(
            screen_name=screen_name,
            count_per_page=10,
            n_pages=2,
            callback=Callback()
        )
        for tweets, kwargs in itr:
            print(f'{len(tweets)} :: ')


if __name__ == '__main__':
    main()
