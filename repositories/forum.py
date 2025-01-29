from utils.repository import SQLALchemyRepository
from models.forum import ForumModel


class ForumRepository(SQLALchemyRepository):
    model = ForumModel