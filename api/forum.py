from fastapi import APIRouter, Request
from fastapi import Depends, Form, status

from typing import Annotated

from services.forum import ForumService
from api.dependencies import forum_service

from services.users import UserService
from api.dependencies import users_service


from deep_translator import GoogleTranslator

import json

forum_router = APIRouter(
    prefix='/forum',
    tags = ['Forum Routes']
)

@forum_router.post('/add_new_forum')
async def add_new_forum(
    forum_repo: Annotated[ForumService, Depends(forum_service)],
    users_service: Annotated[UserService, Depends(users_service)],
    token: str = Form(...),
    year: str = Form(...),
    place: str = Form(...),
    place_eng: str = Form(...)
):
    
    token_check = await users_service.check_cookie(token = token)
    if token_check['status_code'] != 200:
        return {
            'message': 'Not Authorized',
            'status_code': status.HTTP_401_UNAUTHORIZED
        }

    data = {
        'year': year,
        'place': place,
        'place_eng': place_eng
    }

    result = await forum_repo.add_forum(data = data)
    return result

@forum_router.get('/get_forum')
async def get_forum(
    forum_service: Annotated[ForumService, Depends(forum_service)],
    request: Request,
    id: int = None
):

    redis_client = request.app.state.redis

    redis_data = await redis_client.get('forum_data')

    if not redis_data:
        if not id:
            filters = {}
        else:
            filters = {
                'id': id
            } 

        result = await forum_service.get_forum_filters(filters = filters)
        result_list = [

        ]

        for each in result:

            data = {
                "id": each.id,
                "place": each.place,
                'place_eng': each.place_eng,
                "year": each.year
            }

            result_list.append(data)
        
        await redis_client.set('forum_data', json.dumps(result_list))
        await redis_client.expire('forum_data', 3600)
    else:
        result_list = json.loads(redis_data)

    return result_list