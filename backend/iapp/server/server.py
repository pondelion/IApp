from fastapi import FastAPI
from iapp.server.api import api_router
from iapp.settings import settings


app = FastAPI(title='iapp')

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get('/')
def health_check():
    return 'healthy'
