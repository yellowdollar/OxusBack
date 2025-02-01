from fastapi import APIRouter, File, UploadFile, Request
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

import json


news_router = APIRouter(
    prefix = '/news',
    tags = ['News']
)

def split_text(text, max_length=1000):
    # Разделяет текст на части по максимальной длине
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

async def translate_text(text, source_lang='auto', target_lang='en'):
    # Разделение текста на части, учитывая ограничение по символам (например, 1000)
    parts = split_text(text, max_length=1000)
    translated_parts = []

    for part in parts:
        try:
            # Перевод каждой части
            translated_part = GoogleTranslator(source=source_lang, target=target_lang).translate(part)
            translated_parts.append(translated_part)
        except Exception as e:
            print(f"Error during translation: {e}")
            translated_parts.append(part)  # На случай ошибки возвращаем оригинальный текст

    # Объединяем переведенные части обратно в один текст
    return " ".join(translated_parts)

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
    request: Request,
    id: int = None
):
    if not id:
        redis_client = request.app.state.redis
        redis_data = await redis_client.get('news_all')

        if not redis_data:
            all_news = await news_service.get_news(filters={})

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
                    photo_get = await photo_service.get_photo(id=each.photo_id)

                if photo_get == "No Photo":
                    photo_path = photo_get
                else:
                    photo_path = photo_get[0].photo_path

                # Correct the translation by using title and text individually
                title_eng = await translate_text(each.title)
                text_eng = await translate_text(each.text)

                data = {
                    'id': each.id,
                    'title': each.title,
                    'title_eng': title_eng, 
                    'text': each.text,
                    'text_eng': text_eng, 
                    'date': each.date,
                    'photo_path': photo_path
                }

                result.append(data)

            await redis_client.set('news_all', json.dumps(result))
            await redis_client.expire('news_all', 3600)
        else:
            result = json.loads(redis_data)

        return result[::-1]
    else:
        new = await news_service.get_news(filters={'id': id})

        if not new:
            return {
                'message': f'News with id: {id} not found',
                'status_code': status.HTTP_404_NOT_FOUND
            }

        redis_client = request.app.state.redis
        redis_data = await redis_client.get(f'one_new_{id}')

        if not redis_data:
            result = []

            for each in new:
                if each.photo_id is None:
                    photo_get = "No Photo"
                else:
                    photo_get = await photo_service.get_photo(id=each.photo_id)

                if photo_get == "No Photo":
                    photo_path = photo_get
                else:
                    photo_path = photo_get[0].photo_path

                # Correct translation here too
                title_eng = await translate_text(each.title)
                text_eng = await translate_text(each.text)

                data = {
                    'id': each.id,
                    'title': each.title,
                    'title_eng': title_eng, 
                    'text': each.text,
                    'text_eng': text_eng, 
                    'date': each.date,
                    'photo_path': photo_path
                }

                result.append(data)

            await redis_client.set(f'one_new_{id}', json.dumps(result))
            await redis_client.expire(f'one_new_{id}', 3600)
        else:
            result = json.loads(redis_data)

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