from fastapi import APIRouter, File, UploadFile
from fastapi import Form, status, Depends
from fastapi.responses import FileResponse

from typing import List, Annotated

from services.news import NewService
from api.dependencies import news_services

from services.photo import PhotoService
from api.dependencies import photo_service

from services.users import UserService
from api.dependencies import users_service

import jwt
from jwt.exceptions import InvalidTokenError

import os

from datetime import datetime

from deep_translator import GoogleTranslator


news_router = APIRouter(
    prefix = '/news',
    tags = ['News']
)

@news_router.post('/add_new')
async def add_new(
    users_service: Annotated[UserService, Depends(users_service)],
    news_service: Annotated[NewService, Depends(news_services)],
    photo_service: Annotated[PhotoService, Depends(photo_service)],
    token: str = Form(None),
    title: str = Form(None),
    text: str = Form(None),
    photo_files: List[UploadFile] = File(...)
):
    check = await users_service.check_cookie(token)

    if check['status_code'] != 200:
        return {
            'message': 'Not Authorized',
            'status_code': status.HTTP_401_UNAUTHORIZED
        }

    current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M")
    data = {
        'title': title,
        'text': text,
        'date': current_datetime
    }

    result = await news_service.add_new(token=token, data=data)

    if not result:
        return {
            'message': f'Some Error, {result[0].id}',
            'status_code': status.HTTP_400_BAD_REQUEST
        }

    dir_path = f'mock/photos/news/news_{result[0].id}'
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    photo_paths = []

    for index, photo_file in enumerate(photo_files, start=1):
        file_name = f'photo_{index}' + os.path.splitext(photo_file.filename)[1] 
        file_path = os.path.join(dir_path, file_name)
        with open(file_path, "wb") as f:
            content = await photo_file.read()
            f.write(content)
        photo_paths.append(file_path)

    photo_data = {
        'photo_path': ";".join(photo_paths)
    }


    photo_add = await photo_service.add_photo(data = photo_data)

    insert_news_photo_path = await news_service.update_new(id = int(result[0].id), data = {'photo_id': photo_add[0].id})

    return {
        'photo_path': photo_add,
        'news_data': insert_news_photo_path
    }

@news_router.post('/delete_new')
async def delete_new(
    news_service: Annotated[NewService, Depends(news_services)],
    users_service: Annotated[UserService, Depends(users_service)],
    token: str = Form(...),
    id: int = Form(...)
):
    check = await users_service.check_cookie(token)

    if check['status_code'] == 401:
        return {
            'message': 'Not Authorized',
            'status_code': status.HTTP_401_UNAUTHORIZED
        }
    
    news = await news_service.get_news(filters = {'id': id})

    if not news:
        return {
            'message': f'News with id: {id} not found',
            'status_code': status.HTTP_404_NOT_FOUND
        }
    
    delete_item = await news_service.delete_new(id = news[0].id)

    return {
        'message': 'New were deleted',
        'status_code': status.HTTP_200_OK
    }


@news_router.get('/get_all_news')
async def get_all_news(
    news_service: Annotated[NewService, Depends(news_services)],
    photo_service: Annotated[PhotoService, Depends(photo_service)],
    id: int = None
):
    if not id:
        all_news = await news_service.get_news(filters = {})

        if not all_news:
            return {
                'message': 'No News in DB',
                'status_code': status.HTTP_404_NOT_FOUND
            }

        result = []

        for each in all_news:
            if each.photo_id is None:
                photo_get = "No Photo"
            else:
                photo_get = await photo_service.get_photo(id = each.photo_id)
            
            if photo_get == "No Photo":
                photo_path = photo_get
            else:
                photo_path = photo_get[0].photo_path

            data = {
                'id': each.id,
                'title': each.title,
                'title_eng': GoogleTranslator(source = "auto", target = "en").translate(each.title), 
                'text': each.text,
                'text_eng': GoogleTranslator(source = "auto", target = "en").translate(each.text), 
                'date': each.date,
                'photo_path': photo_path
            }

            result.append(data)
        
        return result[::-1]
    else:
        new = await news_service.get_news(filters = {'id': id})
        
        if not new:
            return {
                'message': f'News with id: {id} not found',
                'status_code': status.HTTP_404_NOT_FOUND
            }
        
        result = []

        for each in new:
            if each.photo_id is None:
                photo_get = "No Photo"
            else:
                photo_get = await photo_service.get_photo(id = each.photo_id)
            
            if photo_get == "No Photo":
                photo_path = photo_get
            else:
                photo_path = photo_get[0].photo_path

            data = {
                'id': each.id,
                'title': each.title,
                'title_eng': GoogleTranslator(source = "auto", target = "en").translate(each.title), 
                'text': each.text,
                'text_eng': GoogleTranslator(source = "auto", target = "en").translate(each.text), 
                'date': each.date,
                'photo_path': photo_path
            }

            result.append(data)
        
        return result

@news_router.get('/upload', response_model=dict)
async def upload(
    photo_path: str = None
):
    if not os.path.exists(photo_path) or not os.path.isfile(photo_path):
        return {
            'message': 'Directory or file not found',
            'status_code': status.HTTP_400_BAD_REQUEST
        }
    
    return FileResponse(photo_path)