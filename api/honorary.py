from fastapi import APIRouter
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

from googletrans import Translator


hon_router = APIRouter(
    prefix = '/honorary',
    tags = ['Honorary Routes']
)

translator = Translator()

@hon_router.post('/add_honorary')
async def add_honorary(
    users_service: Annotated[UserService, Depends(users_service)],
    photo_service: Annotated[PhotoService, Depends(photo_service)],
    honorary_service: Annotated[HonoraryService, Depends(honorary_service)],
    token: str = Form(...),
    name: str = Form(...),
    work_place: str = Form(...),
    forum_id: int = Form(...),
    photo: UploadFile = File(...)
):
    check_token = await users_service.check_cookie(token = token)

    if check_token['status_code'] != 200:
        return {
            'message': 'Not Authorized',
            'status_code': status.HTTP_401_UNAUTHORIZED
        }
    
    name_parts = name.split()
    if len(name_parts) < 2:
        return {
            'message': 'Invalid name format. Expected "Surname Name".',
            'status_code': status.HTTP_400_BAD_REQUEST
        }
    
    surname_name = f"{name_parts[0]}_{name_parts[1]}"
    
    base_path = "mock/photos/honorary"
    speaker_path = os.path.join(base_path, surname_name)

    os.makedirs(speaker_path, exist_ok=True)

    _, file_extension = os.path.splitext(photo.filename)
    new_filename = f"{surname_name}{file_extension}"
    file_path = os.path.join(speaker_path, new_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await photo.read())

    photo_data = {
        'photo_path': file_path
    }

    photo_add = await photo_service.add_photo(data=photo_data)

    data = {
        'name': name,
        'work_place': work_place,
        'forum_id': forum_id,
        'photo_id': photo_add[0].id
    }

    result = await honorary_service.add_new_honorary(data = data)
    return result

@hon_router.get('/get_honorary')
async def get_honorary(
    honorary_service: Annotated[HonoraryService, Depends(honorary_service)],
    photo_service: Annotated[PhotoService, Depends(photo_service)],
    forum_id: int
):
    result = await honorary_service.get_all_honorary(forum_id = forum_id)
    
    result_list = []

    for each in result:
        photo = await photo_service.get_photo(id = each.photo_id)

        data = {
            'name': each.name,
            'name_end': translator.translate(each.name, dest = "en").text,
            'work_place': each.work_place,
            'work_place_eng': translator.translate(each.work_place, dest = "en").text,
            'photo_path': photo[0].photo_path
        }

        result_list.append(data)

    return result_list