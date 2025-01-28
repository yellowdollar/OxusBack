from fastapi import FastAPI

from database.database import init_models
from contextlib import asynccontextmanager

from api.news import news_router
from api.auth import users_router

from models.photo import PhotoModel
from models.news import NewsModel

from fastapi.middleware.cors import CORSMiddleware

import json


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield

app = FastAPI(
    lifespan = lifespan,
    root_path='/api',
    openapi_url='/openapi.json',
    docs_url='/docs',
)
app.include_router(router = news_router)
app.include_router(router = users_router)

app.add_middleware ( 
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

