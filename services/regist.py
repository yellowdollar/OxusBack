from utils.repository import AbstractRepository


class RegistService:

    def __init__(self, regist_repo: AbstractRepository):
        self.regist_repo: AbstractRepository = regist_repo()

    async def add_new_regist(self, data):
        result = await self.regist_repo.add(data = data)
        return result
    
    async def get_regists_filters(self):
        result = await self.regist_repo.get(filters = {})
        return result