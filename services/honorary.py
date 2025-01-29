from utils.repository import AbstractRepository


class HonoraryService:

    def __init__(self, hon_repo: AbstractRepository):
        self.hon_repo: AbstractRepository = hon_repo()

    async def add_new_honorary(self, data: dict):
        result = await self.hon_repo.add(data = data)
        return result
    
    async def get_all_honorary(self, forum_id):
        result = await self.hon_repo.get(filters = {'forum_id': forum_id})
        return result
