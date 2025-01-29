from utils.repository import SQLALchemyRepository
from models.program import ProgramModel


class ProgramRepository(SQLALchemyRepository):
    model = ProgramModel