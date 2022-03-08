import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import time

import urllib
import pandas as pd

from iapp.crawler import (
    TwitterFollowerCrawler,
    TwitterFolloweeCrawler,
    TwitterUserCrawler,
)
from iapp.db.dynamodb import DynamoDB
from iapp.storage.s3 import S3
from iapp.utils.config import AWSConfig, DataLocationConfig
from iapp.utils.dynamodb import format_data
from iapp.utils.logger import Logger
from iapp.schemas.twitter import (
    TwitterFollowerCreate as TwitterFollowerScheme,
    TwitterFolloweeCreate as TwitterFolloweeScheme,
    TwitterUser as TwitterUserScheme,
)
from iapp.models.sqlalchemy.twitter import (
    TwitterFollower as TwitterFollowerModel,
    TwitterFollowee as TwitterFolloweeModel,
)
from iapp.repository.rdb import (
    TwitterUserRepository,
    TwitterFollowerRepository,
    TwitterFolloweeRepository,
)
from iapp.db.rdb import db, init_rdb


TAG = 'twitter_user_crawl'
user_repo = TwitterUserRepository()
follower_repo = TwitterFollowerRepository()
followee_repo = TwitterFolloweeRepository()
follower_crawler = TwitterFollowerCrawler()
followee_crawler = TwitterFolloweeCrawler()
user_crawler = TwitterUserCrawler()


def main():
    # init_rdb(recreate_table=True)
    init_rdb()

    screen_name = 'TwitterJP'

    ts1 = datetime.now()
    target_user = user_repo.get_by_screen_name(db, screen_name=screen_name)
    print(target_user)
    ts2 = datetime.now()
    print((ts2-ts1).total_seconds())
    if target_user:
        print(f'user alredy exixts in db : {target_user.__dict__}')
        ts3 = datetime.now()
        elapsed_sec_since_last_update = (ts3-target_user.updated_at).total_seconds()
        print(elapsed_sec_since_last_update)

        followers = follower_crawler.run(user_id_or_screen_name=screen_name, max_count=5)
        print(f'len(followers) : {len(followers)}')
        follower_scheme_list = [TwitterFollowerScheme(user_id=target_user.id, follower_id=follower._json['id']) for follower in followers]
        # for tfs in follower_scheme_list:
        #     Logger.i('follower', f'start user crawl {tfs.follower_id}')
        #     follower_data = user_crawler.run(user_id_or_screen_name=tfs.follower_id)
        #     Logger.i('follower', f'done user crawl {tfs.follower_id}')
        #     tus = TwitterUserScheme.parse_obj(follower_data._json)
        #     Logger.i('follower', f'start insert user to db {tfs.follower_id}')
        #     user_repo.create(db, data=tus, check_already_id_exists=True)
        #     Logger.i('follower', f'done insert user to db {tfs.follower_id}')
        #     Logger.i('follower', f'start insert follower data to db {tfs.follower_id}')
        #     follower_repo.create(
        #         db,
        #         data=tfs,
        #         check_already_exists_filter_conditions=[TwitterFollowerModel.user_id==tfs.user_id, TwitterFollowerModel.follower_id==tfs.follower_id]
        #     )
        #     Logger.i('follower', f'done insert follower data to db {tfs.follower_id}')
        Logger.i('follower', f'start user crawl')
        follower_data_list = [user_crawler.run(user_id_or_screen_name=tfs.follower_id) for tfs in follower_scheme_list]
        Logger.i('follower', f'done user crawl')
        tus_list = [TwitterUserScheme.parse_obj(follower_data._json) for follower_data in follower_data_list]
        Logger.i('follower', f'start insert user to db')
        created_users = user_repo.create_all(db, data_list=tus_list, check_already_id_exists=True)
        Logger.i('follower', f'done insert user to db : len=>{len(created_users)}')
        Logger.i('follower', f'start insert follower data to db')
        # filter_conditions_list = [
        #     [TwitterFollowerModel.user_id==tfs.user_id, TwitterFollowerModel.follower_id==tfs.follower_id] for tfs in follower_scheme_list
        # ]
        created_followers = follower_repo.create_all(
            db,
            data_list=follower_scheme_list,
            # check_already_exists_filter_conditions_list=filter_conditions_list
        )
        Logger.i('follower', f'done insert follower data to db : len=>{len(created_followers)}')

        followees = followee_crawler.run(user_id_or_screen_name=screen_name, max_count=5)
        print(f'len(followees) : {len(followees)}')
        followee_scheme_list = [TwitterFolloweeScheme(user_id=target_user.id, followee_id=followee._json['id']) for followee in followees]
        # for tfs in followee_scheme_list:
        #     followee_data = user_crawler.run(user_id_or_screen_name=tfs.followee_id)
        #     tus = TwitterUserScheme.parse_obj(followee_data._json)
        #     user_repo.create(db, data=tus, check_already_id_exists=True)
        #     followee_repo.create(
        #         db,
        #         data=tfs,
        #         check_already_exists_filter_conditions=[TwitterFolloweeModel.user_id==tfs.user_id, TwitterFolloweeModel.followee_id==tfs.followee_id]
        #     )
        Logger.i('followee', f'start user crawl')
        followee_data_list = [user_crawler.run(user_id_or_screen_name=tfs.followee_id) for tfs in followee_scheme_list]
        Logger.i('followee', f'done user crawl')
        tus_list = [TwitterUserScheme.parse_obj(followee_data._json) for followee_data in followee_data_list]
        Logger.i('followee', f'start insert user to db')
        created_users = user_repo.create_all(db, data_list=tus_list, check_already_id_exists=True)
        Logger.i('followee', f'done insert user to db : len=>{len(created_users)}')
        Logger.i('followee', f'start insert followee data to db')
        # filter_conditions_list = [
        #     [TwitterFolloweeModel.user_id==tfs.user_id, TwitterFolloweeModel.followee_id==tfs.followee_id] for tfs in followee_scheme_list
        # ]
        created_followees = followee_repo.create_all(
            db,
            data_list=followee_scheme_list,
            # check_already_exists_filter_conditions_list=filter_conditions_list
        )
        Logger.i('followee', f'done insert followee data to db : len=>{len(created_followees)}')
    else:
        print(f'User {screen_name} does not exists in db, crawl user info first.')


if __name__ == '__main__':
    main()
