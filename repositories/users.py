from utils.repository import SQLALchemyRepository
from models.users import UserModel


class UserRepository(SQLALchemyRepository):
    model = UserModel