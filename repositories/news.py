from utils.repository import SQLALchemyRepository
from models.news import NewsModel

class NewsRepository(SQLALchemyRepository):
    model = NewsModel