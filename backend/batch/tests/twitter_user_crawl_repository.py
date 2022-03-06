import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
from iapp.db.rdb import db, init_rdb


TAG = 'twitter_user_crawl'
tur = TwitterUserRepository()


class Callback(TwitterUserCrawler.Callback):

    def on_finished(self, data, args):
        Logger.d(TAG, 'on_finished')
        # print(data)
        print(args)

        items = format_data(data._json)
        # print(items['created_at'])
        # items['account_created_at'] = pd.to_datetime(items['created_at'])
        tus = TwitterUserScheme.parse_obj(items)
        print(tus)
        target_user = tur.get_by_screen_name(db, screen_name=args['user_id_or_screen_name'])
        if target_user:
            # 更新
            updated = tur.update_by_filter(
                db,
                filter_condition=TwitterUserModel.screen_name==args['user_id_or_screen_name'],
                update_data=tus
            )
            print(f'updated record : {updated}')
        else:
            # 追加
            tur.create(db, data=tus)
            print(f'added new record : {tus}')

        # print(items)

    def on_failed(self, e, args):
        Logger.e(TAG, f'on_failed : {e} : {args}')


def main():
    init_rdb(recreate_table=True)
    # init_rdb()
    uc = TwitterUserCrawler()

    screen_name = 'TwitterJP'

    ts1 = datetime.now()
    target_user = tur.get_by_screen_name(db, screen_name=screen_name)
    print(target_user)
    ts2 = datetime.now()
    print((ts2-ts1).total_seconds())
    if target_user:
        print(f'user alredy exixts in db : {target_user.__dict__}')
        ts3 = datetime.now()
        elapsed_sec_since_last_update = (ts3-target_user.updated_at).total_seconds()
        print(elapsed_sec_since_last_update)
        if elapsed_sec_since_last_update > 60:
            print('Over 60 sec passed since last updated. Re-crawling.')
            uc.run(
                user_id_or_screen_name=screen_name,
                callback=Callback()
            )
    else:
        uc.run(
            user_id_or_screen_name=screen_name,
            callback=Callback()
        )


if __name__ == '__main__':
    main()
