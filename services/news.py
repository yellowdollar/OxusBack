from utils.repository import AbstractRepository

import json

import jwt
from jwt.exceptions import InvalidTokenError


with open('config.json', 'r', encoding = 'utf-8') as file:
    data = json.load(file)
    SECRET_KEY = data['SECRET_KEY']
    ALGORITHM = data['ALGORITHM']


class NewService:

    def __init__(self, news_repo: AbstractRepository):
        self.news_repo: AbstractRepository = news_repo()

    async def add_new(self, token: str, data: dict):

        try:
            to_decode = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user_id = to_decode.get('id')

            if not user_id:
                return {
                    'messsage': 'Not Authorized',
                    'status_code': 401
                }
        except InvalidTokenError:
            return {
                'message': 'Ivalid Token Error',
                'status_code': 401
            }

        result = await self.news_repo.add(data = data)
        return result
    
    async def update_new(self, id: int, data: dict):
        result = await self.news_repo.update(id = id, data = data)
        return result
    
    async def get_news(self, filters):
        if not filters:
            result = await self.news_repo.get(filters = {})
            return result
        else:
            result = await self.news_repo.get(filters = filters)
            return result
        
    async def delete_new(self, id):
        result = await self.news_repo.delete(id = id)
        return result