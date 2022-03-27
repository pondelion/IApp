from fastapi import APIRouter

from .routes import (
    twitter,
)


api_router = APIRouter()
api_router.include_router(twitter.router, prefix='/twitter', tags=['twitter'])
