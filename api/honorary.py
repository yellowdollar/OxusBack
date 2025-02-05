from fastapi import APIRouter, Request
from fastapi import Depends, Form, status
from fastapi import UploadFile, File

from api.dependencies import users_service
from services.users import UserService

from api.dependencies import photo_service
from services.photo import PhotoService

from api.dependencies import honorary_service
from services.honorary import HonoraryService

from typing import Annotated

import os

from deep_translator import GoogleTranslator

import json


hon_router = APIRouter(
    prefix = '/honorary',
    tags = ['Honorary Routes']
)

@hon_router.post('/add_honorary')
async def add_honorary(
    users_service: Annotated[UserService, Depends(users_service)],
    photo_service: Annotated[PhotoService, Depends(photo_service)],
    honorary_service: Annotated[HonoraryService, Depends(honorary_service)],
    token: str = Form(...),
    name: str = Form(...),
    name_eng: str = Form(...),
    work_place: str = Form(...),
    work_place_eng: str = Form(...),
    forum_id: int = Form(...),
    photo: UploadFile = File(...)
):
    check_token = await users_service.check_cookie(token=token)

    if check_token['status_code'] != 200:
        return {
            'message': 'Not Authorized',
            'status_code': status.HTTP_401_UNAUTHORIZED
        }

    # Заменяем все пробелы в name на "_"
    name_formatted = name.replace(" ", "_")

    # Создаем путь к папке
    base_path = "mock/photos/honorary"
    speaker_path = os.path.join(base_path, name_formatted)

    os.makedirs(speaker_path, exist_ok=True)

    _, file_extension = os.path.splitext(photo.filename)
    new_filename = f"{name_formatted}{file_extension}"
    file_path = os.path.join(speaker_path, new_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await photo.read())

    photo_data = {
        'photo_path': file_path
    }

    photo_add = await photo_service.add_photo(data=photo_data)

    data = {
        'name': name,
        'name_eng': name_eng,
        'work_place': work_place,
        'work_place_eng': work_place_eng,
        'forum_id': forum_id,
        'photo_id': photo_add[0].id
    }

    result = await honorary_service.add_new_honorary(data=data)
    return result

@hon_router.get('/get_honorary')
async def get_honorary(
    honorary_service: Annotated[HonoraryService, Depends(honorary_service)],
    photo_service: Annotated[PhotoService, Depends(photo_service)],
    request: Request,
    forum_id: int
):
    
    redis_client = request.app.state.redis

    redis_data = await redis_client.get('honorary')

    if not redis_data:
        result = await honorary_service.get_all_honorary(forum_id = forum_id)
        
        result_list = []

        for each in result:
            photo = await photo_service.get_photo(id = each.photo_id)

            data = {
                'name': each.name,
                'name_end': each.name_eng,
                'work_place': each.work_place,
                'work_place_eng': each.work_place_eng,
                'photo_path': photo[0].photo_path
            }

            result_list.append(data)

        await redis_client.set('honorary', json.dumps(result_list))
        await redis_client.expire('honorary', 3600)
    else:
        result_list = json.loads(redis_data)

    return result_list