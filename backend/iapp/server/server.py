from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from iapp.server.api import api_router
from iapp.settings import settings

from .api.deps.auth import get_current_user

app = FastAPI(title='iapp')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.DISABLE_AUTH:
    async def disable_auth_dep(ppp: Optional[int] = None):
        return ppp
    app.dependency_overrides[get_current_user] = disable_auth_dep

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get('/')
def health_check():
    return 'healthy'
