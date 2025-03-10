from fastapi import FastAPI

from database.database import init_models
from contextlib import asynccontextmanager

from api.news import news_router
from api.auth import users_router
from api.forum import forum_router
from api.speakers import speakers_router
from api.honorary import hon_router
from api.program import program_router
from api.regist import regist_router

from models.photo import PhotoModel
from models.news import NewsModel

from fastapi.middleware.cors import CORSMiddleware

import json
from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.redis = Redis(host='localhost', port=6379, decode_responses=True, db=0)

    await init_models()
    yield

    await app.state.redis.close()

app = FastAPI(
    lifespan = lifespan,
    root_path='/api',
    openapi_url=None,
    docs_url=None,
)
app.include_router(router = news_router)
app.include_router(router = users_router)
app.include_router(router = forum_router)
app.include_router(router = speakers_router)
app.include_router(router = hon_router)
app.include_router(router = program_router)
app.include_router(router = regist_router)

app.add_middleware ( 
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)