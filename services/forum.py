from utils.repository import AbstractRepository

import json

import jwt
from jwt.exceptions import InvalidTokenError


class ForumService:

    def __init__(self, forum_repo: AbstractRepository):
        self.forum_repo: AbstractRepository = forum_repo()

    async def add_forum(self, data: dict):
        result = await self.forum_repo.add(data = data)
        return result
    
    async def get_forum_filters(self, filters):
        result = await self.forum_repo.get(filters = filters)
        return result
        