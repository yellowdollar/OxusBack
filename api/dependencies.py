from services.news import NewService
from repositories.news import NewsRepository

from services.users import UserService
from repositories.users import UserRepository

from services.photo import PhotoService
from repositories.photo import PhotoRepositories

from services.forum import ForumService
from repositories.forum import ForumRepository

from services.speakers import SpeakersService
from repositories.speakers import SpeakersRepository

def news_services():
    return NewService(NewsRepository)

def users_service():
    return UserService(UserRepository)

def photo_service():
    return PhotoService(PhotoRepositories)

def forum_service():
    return ForumService(ForumRepository)

def speakers_service():
    return SpeakersService(SpeakersRepository)