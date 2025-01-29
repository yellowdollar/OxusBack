from utils.repository import AbstractRepository

import jwt
from jwt.exceptions import InvalidTokenError

import json

with open('config.json', 'r', encoding = 'utf-8') as file:
    data = json.load(file)
    SECRET_KEY = data['SECRET_KEY']
    ALGORITHM = data['ALGORITHM']


class PhotoService:

    def __init__(self, photo_service: AbstractRepository):
        self.photo_service: AbstractRepository = photo_service()

    async def add_photo(self, data: dict):
        result = await self.photo_service.add(data = data)
        return result

    async def get_photo(self, id):
        result = await self.photo_service.get(filters = {'id': id})
        return result

    