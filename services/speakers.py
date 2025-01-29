from utils.repository import AbstractRepository


class SpeakersService:

    def __init__(self, speaker_repo: AbstractRepository):
        self.speaker_repo: AbstractRepository = speaker_repo()

    async def add_speaker(self, data: dict):
        result = await self.speaker_repo.add(data = data)
        return result

    async def get_speakers_filters(self, filters: dict):
        result = await self.speaker_repo.get(filters = filters)
        return result 