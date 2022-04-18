from datetime import datetime, timedelta
from fastapi import HTTPException, status

from constants import ACCESS_TOKEN_DATA, REFRESH_TOKEN_DATA
from .interfaces.token_service_interface import TokenServiceInterface
from jose import jwt, JWTError
from settings import get_settings


class TokenService(TokenServiceInterface):
    def __init__(self):
        self._settings = get_settings()

    async def create_token(self, email: str, secret_key: str, algorithm: str, token_type: str, exp_time: int) -> str:
        expire_time = datetime.utcnow() + timedelta(minutes=exp_time)
        data = {'sub': email, 'exp': expire_time, 'token_type': token_type}
        return jwt.encode(data, key=secret_key, algorithm=algorithm)

    async def decode_access_token(self, access_token: str, secret_key: str, algorithm: str) -> dict:
        try:
            payload: dict = jwt.decode(token=access_token, key=secret_key, algorithms=algorithm)
            if payload.get('token_type') == 'access_token':
                return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Access token expired')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials',
                                headers={"WWW-Authenticate": "Bearer"})

    async def decode_refresh_token(self, refresh_token: str, secret_key: str, algorithm: str):
        try:
            payload: dict = jwt.decode(token=refresh_token, key=secret_key, algorithms=algorithm)
            if payload.get('token_type') != 'refresh_token':
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid type for token')
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token expired')
        except jwt.JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')


class CreateTokensMixin:
    @staticmethod
    async def create_tokens(email: str, token_service: TokenServiceInterface):
        access_token = await token_service.create_token(email=email, token_type='access_token', **ACCESS_TOKEN_DATA)
        refresh_token = await token_service.create_token(email=email, token_type='refresh_token', **REFRESH_TOKEN_DATA)
        return {'access_token': access_token, 'refresh_token': refresh_token}
