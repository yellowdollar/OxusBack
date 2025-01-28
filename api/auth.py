from fastapi import APIRouter
from fastapi import Depends, status, Form

from typing import Annotated

from api.dependencies import users_service
from services.users import UserService

users_router = APIRouter(
    prefix = '/auth',
    tags = ['User Auth']
)

@users_router.post('/create_user')
async def create_user(
    users_service: Annotated[UserService, Depends(users_service)],
    login: str = Form(...),
    password: str = Form(...)
):
    result = await users_service.add_user(login = login, password = password)
    return result

@users_router.post('/sign_in')
async def sign_in(
    users_service: Annotated[UserService, Depends(users_service)],
    login: str = Form(...),
    password: str = Form(...)
):
    result = await users_service.sign_in(login = login, password = password)
    return result

@users_router.post('/check_cookie')
async def check_cookie(
    users_service: Annotated[UserService, Depends(users_service)],
    token: str = Form(...)
):
    check = await users_service.check_cookie(token)
    return check