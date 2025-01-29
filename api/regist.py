from fastapi import APIRouter
from fastapi import Depends, Form, status

from api.dependencies import users_service
from services.users import UserService

from api.dependencies import regist_service
from services.regist import RegistService

from typing import Annotated


regist_router = APIRouter(
    prefix = '/regist',
    tags = ['Regist Routes']
)

@regist_router.post('/add_regist')
async def add_regist(
    regist_service: Annotated[RegistService, Depends(regist_service)],
    name: str = Form(None),
    surname: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    smth: str = Form(None)
):
    data = {
        'name': name,
        'surname': surname,
        'email': email,
        'phone': phone,
        'smth': smth
    }

    result = await regist_service.add_new_regist(data = data)

    return {
        'status_code': status.HTTP_200_OK,
        'data': result
    }

@regist_router.get('/get_regists')
async def get_regists(
    users_service: Annotated[UserService, Depends(users_service)],
    regist_service: Annotated[RegistService, Depends(regist_service)],
    token: str = ...
):
    check_token = await users_service.check_cookie(token)

    if check_token['status_code'] != 200:
        return {
            'message': 'Not Authorized',
            'status_code': status.HTTP_401_UNAUTHORIZED
        }
    
    regists = await regist_service.get_regists_filters()
    return regists