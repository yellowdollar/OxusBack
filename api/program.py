from fastapi import APIRouter, Request
from fastapi import Depends, Form, status

from api.dependencies import users_service
from services.users import UserService

from api.dependencies import program_service
from services.program import ProgramService

from typing import Annotated

from deep_translator import GoogleTranslator

import json

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
    request: Request,
    forum_id: int = ...,
):
    redis_client = request.app.state.redis

    if not redis_client:
        return {"message": "Redis not initialized", "status_code": 500}

    redis_data = await redis_client.get('data')

    if not redis_data:
        result = await program_service.get_program_filters(forum_id = forum_id)
        result_list = []

        for each in result:

            data = {
                'id': each.id,
                'name': each.name,
                'time': each.time,
                'title': each.title,
                'title_eng': GoogleTranslator(source="auto", target="en").translate(each.title),
                'text': each.text,
                'text_eng': GoogleTranslator(source = "auto", target = "en").translate(each.text),
                'forum_id': forum_id
            }

            result_list.append(data)
        
        await redis_client.set('data', json.dumps(result_list))
        await redis_client.expire('data', 3600)
    else:        
        result_list = json.loads(redis_data)

    return result_list