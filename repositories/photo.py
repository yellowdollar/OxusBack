from utils.repository import SQLALchemyRepository
from models.photo import PhotoModel


class PhotoRepositories(SQLALchemyRepository):
    model = PhotoModel