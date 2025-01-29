from utils.repository import SQLALchemyRepository
from models.speakers import SpeakersModel


class SpeakersRepository(SQLALchemyRepository):
    model = SpeakersModel