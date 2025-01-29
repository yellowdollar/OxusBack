from utils.repository import SQLALchemyRepository
from models.honorary import HonoraryModel


class HonoraryRepository(SQLALchemyRepository):
    model = HonoraryModel