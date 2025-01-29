from fastapi import APIRouter
from fastapi import Depends, Form, status

from api.dependencies import users_service
from services.users import UserService

from api.dependencies import program_service
from services.program import ProgramService

from typing import Annotated


program_router = APIRouter(
    prefix = '/program',
    tags = ['Program Routes']
)

@program_router.post('/add_program')
async def add_program(
    users_service: Annotated[UserService, Depends(users_service)],
    program_service: Annotated[ProgramService, Depends(program_service)],
    token: str = Form(...),
    name: str = Form(...),
    time: str = Form(...),
    title: str = Form(...),
    text: str = Form(...),
    forum_id: int = Form(...)
):
    check_token = await users_service.check_cookie(token)

    if check_token['status_code'] != 200:
        return {
            'message': 'Not Authorized',
            'status_code': status.HTTP_401_UNAUTHORIZED
        }
    
    data = {
        'name': name,
        'time': time,
        'title': title,
        'text': text,
        'forum_id': forum_id
    }

    result = await program_service.add_new_program(data = data)
    return result

@program_router.get('/get_program')
async def get_program(
    program_service: Annotated[ProgramService, Depends(program_service)],
    forum_id: int = ...
):
    result = await program_service.get_program_filters(forum_id = forum_id)
    return result