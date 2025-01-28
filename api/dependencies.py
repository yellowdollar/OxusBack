from services.news import NewService
from repositories.news import NewsRepository

from services.users import UserService
from repositories.users import UserRepository

from services.photo import PhotoService
from repositories.photo import PhotoRepositories

def news_services():
    return NewService(NewsRepository)

def users_service():
    return UserService(UserRepository)

def photo_service():
    return PhotoService(PhotoRepositories)