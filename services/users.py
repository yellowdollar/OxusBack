from utils.repository import AbstractRepository
from repositories.users import UserModel

from passlib.context import CryptContext

import jwt
from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta

import json


with open('config.json', 'r', encoding = 'utf-8') as file:
    data = json.load(file)
    SECRET_KEY = data['SECRET_KEY']
    ALGORITHM = data['ALGORITHM']

def create_access_token(data: dict, expires_delta: timedelta):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=10800)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

class UserService:

    def __init__(self, users_repo: AbstractRepository):
        self.user_repo: AbstractRepository = users_repo()

    async def add_user(self, login, password):
        hashed_password = pwd_context.hash(password)

        data = {
            'login': login,
            'password': hashed_password
        }

        result = await self.user_repo.add(data = data)
        return result
    
    async def sign_in(self, login, password):
        user_db = await self.user_repo.get(filters = {'login': login})
        if not user_db:
            return {
                'message': f'User with login: {login} not found',
                'status_code': 404
            }
        
        user_password = user_db[0].password

        if not verify_password(password, user_password):
            return {
                'message': 'Wrong Password',
                'status_code': 400
            }
        
        token_data = {
            'id': user_db[0].id,
            'login': user_db[0].login
        }        
        access_token_expires = timedelta(minutes = 10800)    
        
        jwt_token = create_access_token(data = token_data, expires_delta = access_token_expires)
        return {
            'message': 'OK',
            'status_code': 200,
            'token': jwt_token,
            'token_type': 'bearer'
        }
    
    async def check_cookie(self, token):
        try:
            to_decode = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user_id = to_decode.get('id')

            check = await self.user_repo.get(filters = {'id': user_id})

            if not check:
                return {
                    'messsage': 'Not Authorized',
                    'status_code': 401
                }
            
            return {
                'message': 'Authorized',
                'status_code': 200
            }
        except InvalidTokenError:
            return {
                'message': 'Ivalid Token Error',
                'status_code': 401
            }