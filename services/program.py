from utils.repository import AbstractRepository


class ProgramService:

    def __init__(self, program_repo: AbstractRepository):
        self.program_repo: AbstractRepository = program_repo()

    async def add_new_program(self, data: dict):
        result = await self.program_repo.add(data)
        return result
    
    async def get_program_filters(self, forum_id: int):
        result = await self.program_repo.get(filters = {'forum_id': forum_id})
        return result