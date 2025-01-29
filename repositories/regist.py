from utils.repository import SQLALchemyRepository
from models.regist import RegistModel


class RegistRepository(SQLALchemyRepository):
    model = RegistModel