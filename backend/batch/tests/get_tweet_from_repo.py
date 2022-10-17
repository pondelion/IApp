from iapp.db.rdb import db
from iapp.repository.rdb import TwitterTweetRepository

ttr = TwitterTweetRepository()
tweets = ttr.get_latest_tweet(db=db, user_id=11)
print(tweets.__dict__)
