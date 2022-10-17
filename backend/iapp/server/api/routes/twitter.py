from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cloudauth.cognito import CognitoClaims

from .... import schemas
from ....service.twitter import (TwitterMediaService, TwitterTweetService,
                                 TwitterUserService)
from ..deps import auth

router = APIRouter()
tus = TwitterUserService()
tts = TwitterTweetService()
tms = TwitterMediaService()

@router.get('/tweet/{user_name}', response_model=List[schemas.twitter.TwitterTweetInDB])
def get_tweet(
    user_name: str,
    count: int = 50,
    current_user: CognitoClaims = Depends(auth.get_current_user),
) -> List[schemas.twitter.TwitterTweetInDB]:
    tweets = tts.get_tweet_by_screen_name(screen_name=user_name, count=count)
    return tweets if tweets else []


@router.get('/user/{user_name}', response_model=Optional[schemas.twitter.TwitterUserInDB])
def get_user(
    user_name: str,
    current_user: CognitoClaims = Depends(auth.get_current_user),
) -> Optional[schemas.twitter.TwitterUserInDB]:
    user = tus.get_user_by_screen_name(screen_name=user_name)
    return user


@router.get('/media', response_model=List[schemas.twitter.TwitterMediaInDB])
def get_media(
    user_name: Optional[str] = None,
    user_id: Optional[int] = None,
    tweet_id: Optional[int] = None,
    current_user: CognitoClaims = Depends(auth.get_current_user),
) -> Optional[schemas.twitter.TwitterMediaInDB]:
    if all([p is None for p in [user_name, user_id, tweet_id]]):
        raise HTTPException(
            status_code=400,
            detail='either user_name, user_id, tweet_id query parameter must be specified.'
        )
    medias = None
    if user_id is not None:
        medias = tms.get_by_user_id(id=user_id)
    elif tweet_id is not None:
        medias = tms.get_by_tweet_id(tweet_id=tweet_id)
    elif user_name is not None:
        medias = tms.get_by_user_name(user_name=user_name)
    return medias if medias else []


@router.get('/health_check')
def health_check():
    return 'ok'
