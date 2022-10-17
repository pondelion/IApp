import pandas as pd
from fastapi.encoders import jsonable_encoder
from iapp.crawler import TwitterUserTweetCrawler
from iapp.models.sqlalchemy.twitter import TwitterTweet as TwitterTweetModel
from iapp.schemas.twitter import TwitterTweet as TwitterTweetSchema

kwargs = {
    'screen_name': 'TwitterJP',
    'count_per_page': 1,
    'n_pages': 1
}
utc = TwitterUserTweetCrawler()
tweets, kwargs = utc.run(**kwargs)
# print(tweets)

# tweets = format_data(tweets._json)
tweets = tweets[0]._json
tweets.update({'screen_name': 'TwitterJP'})
tweets.update({'tweet_created_at': pd.to_datetime(tweets['created_at'])})
tweets.update({'user_id': tweets['user']['id']})
tweets.update({'has_media_files': True if 'media' in tweets['entities'] else False})

scm = TwitterTweetSchema.parse_obj(tweets)
print(scm)

mdl = TwitterTweetModel(**jsonable_encoder(scm))
print(mdl.__dict__)
