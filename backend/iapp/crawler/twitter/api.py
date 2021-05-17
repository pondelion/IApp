import tweepy
from requests_oauthlib import OAuth1Session

from ...utils.config import TwitterConfig


_tweepy_auth = tweepy.OAuthHandler(
    TwitterConfig.CONSUMER_KEY,
    TwitterConfig.CONSUMER_SECRET
)
_tweepy_auth.set_access_token(
    TwitterConfig.ACCESS_TOKEN_KEY,
    TwitterConfig.ACCESS_TOKEN_SECRET,
)

TWEEPY_API = tweepy.API(_tweepy_auth)

TWITTER_API = OAuth1Session(
    TwitterConfig.CONSUMER_KEY,
    TwitterConfig.CONSUMER_SECRET,
    TwitterConfig.ACCESS_TOKEN_KEY,
    TwitterConfig.ACCESS_TOKEN_SECRET
)
