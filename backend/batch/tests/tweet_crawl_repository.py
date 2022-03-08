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
from iapp.schemas.twitter import (
    TwitterTweetInDB as TwitterTweetSchema,
    TwitterMediaInDB as TwitterMediaScheme,
)
from iapp.models.sqlalchemy.twitter import TwitterTweet as TwitterTweetModel
from iapp.repository.rdb import (
    TwitterTweetRepository,
    TwitterUserRepository,
    TwitterMediaRepository,
)
from iapp.db.rdb import db, init_rdb


TAG = 'twitter_tweet_crawl'
tur = TwitterUserRepository()
ttr = TwitterTweetRepository()
tmr = TwitterMediaRepository()
bucket = S3()


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
            data = ttr.create(db, data=tts, check_already_exists=True)
            print(f'saved')

        # Save media files
        for item in items:
            if 'media' not in item['entities']:
                continue
            tweet_id = item['id']
            user_id = item['user']['id']
            medias = item['entities']['media']
            s3_media_urls = []
            for media in medias:
                try:
                    media_id = media['id']
                    media_type = media['type']
                    media_url = media['media_url']
                    filename = media_url.split("/")[-1]
                    local_tmp_filepath = f'/tmp/{filename}'
                    urllib.request.urlretrieve(media_url, local_tmp_filepath)
                    s3_filepath = os.path.join(
                        DataLocationConfig.TWITTER_MEDIAFILE_DIR,
                        f'{user_id}',
                        filename,
                    )
                    bucket.save(local_tmp_filepath, s3_filepath)
                    os.remove(local_tmp_filepath)
                    Logger.d(TAG, f'Saved media file to {s3_filepath}')
                    s3_media_urls.append(s3_filepath)
                    tms = TwitterMediaScheme(
                        id=media_id,
                        tweet_id=tweet_id,
                        user_id=user_id,
                        media_url=media_url,
                        media_s3_url=s3_filepath,
                        media_type=media_type,
                    )
                    tmr.upsert(db, data=tms)
                except Exception as e:
                    print(e)
                    raise e

        # Update user last_tweet_id
        user_id = items[0]['user']['id']
        latest_tweet_id = ttr.get_latest_tweet(db, user_id=user_id)
        print(f'latest_tweet_id : {latest_tweet_id}')
        target_user = tur.get_by_id(db, id=user_id)
        tur.update(db, db_data=target_user, update_data={'last_tweet_id': latest_tweet_id})

        # DynamoDB.put_items(
        #     AWSConfig.DYNAMODB_TWITTER_USER_TWEET_TABLE_NAME,
        #     items,
        # )

    def on_failed(self, e, args):
        Logger.e(TAG, f'on_failed : {e} : {args}')
        raise e


def main():
    # init_rdb(recreate_table=True)
    init_rdb()
    utc = TwitterUserTweetCrawler()

    screen_name = 'TwitterJP'

    ts1 = datetime.now()
    target_user = tur.get_by_screen_name(db, screen_name=screen_name)
    if not target_user:
        print(f'User data {screen_name} does not exists in DB, crawl user data before tweet crawling')
        return
    # target_tweets = ttr.get_by_user_id(db, user_id=target_user.id)
    print(f'target_user : {target_user.__dict__}')
    # print(f'tweets : {target_tweets}')
    ts2 = datetime.now()
    print((ts2-ts1).total_seconds())
    if target_user.last_tweet_id:
        ts3 = datetime.now()
        elapsed_sec_since_last_update = (ts3-target_user.updated_at).total_seconds()
        print(elapsed_sec_since_last_update)
        if elapsed_sec_since_last_update > 60:
            print('Over 60 sec passed since updated. Re-crawling.')
            itr = utc.run_generator(
                screen_name=screen_name,
                count_per_page=5,
                n_pages=2,
                callback=Callback(),
                since_id=target_user.last_tweet_id,
            )
            for tweets, kwargs in itr:
                print(f'{len(tweets)} :: {kwargs}')
    else:
        print('No tweets record found')
        itr = utc.run_generator(
            screen_name=screen_name,
            count_per_page=10,
            n_pages=2,
            callback=Callback()
        )
        for tweets, kwargs in itr:
            print(f'{len(tweets)} :: {kwargs}')


if __name__ == '__main__':
    main()
