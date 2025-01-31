from fastapi import APIRouter
from fastapi import  Depends, Form, status
from fastapi import UploadFile, File

from api.dependencies import speakers_service
from services.speakers import SpeakersService

from api.dependencies import users_service
from services.users import UserService

from api.dependencies import photo_service
from services.photo import PhotoService

from typing import Annotated

import os

from deep_translator import GoogleTranslator


speakers_router = APIRouter(
    prefix = '/speakers',
    tags = ['Speakers Routes']
)

@speakers_router.post('/add_new_speaker')
async def add_new_speaker(
    users_service: Annotated[UserService, Depends(users_service)],
    speakers_service: Annotated[SpeakersService, Depends(speakers_service)],
    photo_service: Annotated[PhotoService, Depends(photo_service)],
    token: str = Form(...),
    name: str = Form(...),
    work_place: str = Form(...),
    forum_id: int = Form(...),
    photo: UploadFile = File(...)
):
    check_token = await users_service.check_cookie(token)

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
    
    base_path = "mock/photos/speakers"
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

    result = await speakers_service.add_speaker(data=data)
    return result

@speakers_router.get('/get_speakers')
async def get_speakers(
    speakers_service: Annotated[SpeakersService, Depends(speakers_service)],
    photo_service: Annotated[PhotoService, Depends(photo_service)],
    id: int = ...
):
    filters = {
        'forum_id': id
    }

    result = await speakers_service.get_speakers_filters(filters = filters)

    result_list = []
    for each in result:
        photo = await photo_service.get_photo(id = each.photo_id)

        data = {
            'id': each.id,
            'name': each.name,
            'name_eng': GoogleTranslator(source="auto", target="en").translate(each.name),
            'work_place': each.work_place,
            'work_place_eng': GoogleTranslator(source="auto", target="en").translate(each.work_place),
            'photo_path': photo[0].photo_path
        }

        result_list.append(data);

    return result_list
