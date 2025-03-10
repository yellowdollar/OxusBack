from fastapi import APIRouter, Depends, Form, status
import aiosmtplib
from email.message import EmailMessage

from api.dependencies import users_service
from services.users import UserService

from api.dependencies import regist_service
from services.regist import RegistService

from typing import Annotated

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "jewelrysanoattj@gmail.com"
SMTP_PASSWORD = "ibqv lwyq hace zauw"

RECIPIENT_EMAIL = "jewelrysanoattj@gmail.com"

regist_router = APIRouter(
    prefix='/regist',
    tags=['Regist Routes']
)

async def send_email_notification(
    name: str, surname: str, 
    email: str, job_title: str, 
    phone: str, smth: str
):
    """Функция отправки email при регистрации"""
    msg = EmailMessage()
    msg["From"] = SMTP_USERNAME
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = "Новый запрос на регистрацию"

    msg.set_content(
        f"Новая регистрация:\n\n"
        f"ФИО: {name} {surname}\n"
        f"Email: {email}\n"
        f"Телефон: {phone}\n"
        f"Должность: {job_title}\n"
        f"Страна/Компания: {smth}"
    )

    await aiosmtplib.send(
        msg,
        hostname=SMTP_SERVER,
        port=SMTP_PORT,
        start_tls=True,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD
    )

@regist_router.post('/add_regist')
async def add_regist(
    regist_service: Annotated[RegistService, Depends(regist_service)],
    name: str = Form(None),
    surname: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    job_title: str = Form(None),
    smth: str = Form(None)
):
    data = {
        'name': name,
        'surname': surname,
        'email': email,
        'phone': phone,
        'job_title': job_title,
        'smth': smth
    }

    result = await regist_service.add_new_regist(data=data)

    # Отправляем email
    await send_email_notification(name, surname, email, job_title, phone, smth)

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
