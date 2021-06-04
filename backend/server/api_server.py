import os
from typing import List, Union, Optional, Any, Dict

from pydantic import BaseModel
from fastapi import FastAPI, Depends, Path, WebSocket
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims
from overrides import overrides

from iapp.resopitory.twitter import (
    UserRepository,
    TweetRepository
)


app = FastAPI()
auth = Cognito(region=os.environ["REGION"], userPoolId=os.environ["USERPOOLID"])


get_current_user = CognitoCurrentUser(
    region=os.environ["REGION"],
    userPoolId=os.environ["USERPOOLID"]
)
twitter_user_repo = UserRepository()
twitter_tweet_repo = TweetRepository()


class TwitterTweetCallback(Callback):

    def __init__(self, ws: WebSocket):
        super().__init__()
        self._ws = ws

    @overrides
    def on_completed(
        self,
        data: Any,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> None:
        print('done fetching tweet')

    @overrides
    def on_progressed(
        self,
        data: Any,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> ProgressResponse:
        await self._ws.send_json({
            'data_no': kwargs['page'],
            'data': data
        })
        print(f'sent data, page : {kwargs["page"]}')
        data = await self._ws.receive_text()
        return ProgressResponse.KEEP_CRAWLING

    @overrides
    def on_failed(
        self,
        e: Exception,
        kwargs: Dict[str, Union[str, int, float]]
    ) -> None:
        print(e)


@app.get("/twitter_user/{screen_name}")
def twitter_user(
    current_user: CognitoClaims = Depends(get_current_user),
    screen_name: str = Path(..., title="The screen name of the twitter user"),
):
    print(current_user.username)
    twitter_user = twitter_user_repo.find(screen_name=screen_name)
    return twitter_user.json()


@app.websocket("/twitter_tweet/{screen_name}")
async def twitter_tweet(
    websocket: WebSocket,
    current_user: CognitoClaims = Depends(get_current_user),
    screen_name: str = Path(..., title="The screen name of the twitter user"),
):
    print(current_user.username)
    await websocket.accept()
    callback = TwitterTweetCallback(websocket)
    _ = twitter_tweet_repo.find(
        screen_name=screen_name,
        callback=callback
    )
