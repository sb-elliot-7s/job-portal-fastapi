from datetime import datetime, timedelta
from fastapi import HTTPException, status
from constants import ACCESS_TOKEN_DATA, REFRESH_TOKEN_DATA
from .interfaces.token_service_interface import TokenServiceInterface
from jose import jwt, JWTError
from settings import get_settings
from common_enums import TokenType


def token_exception_decorator(token_type: str, error_detail: str, headers: dict = None):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'{token_type.capitalize()} expired')
            except JWTError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_detail, headers=headers)
        return wrapper
    return decorator


class TokenService(TokenServiceInterface):
    def __init__(self):
        self._settings = get_settings()

    async def create_token(self, email: str, secret_key: str, algorithm: str, token_type: str, exp_time: int) -> str:
        expire_time = datetime.utcnow() + timedelta(minutes=exp_time)
        data = {'sub': email, 'exp': expire_time, 'token_type': token_type}
        return jwt.encode(data, key=secret_key, algorithm=algorithm)

    @token_exception_decorator(token_type=TokenType.ACCESS_TOKEN.value, error_detail='Could not validate credentials',
                               headers={'WWW-Authenticate': 'Bearer'})
    async def decode_access_token(self, access_token: str, secret_key: str, algorithm: str) -> dict:
        payload: dict = jwt.decode(token=access_token, key=secret_key, algorithms=algorithm)
        if payload.get('token_type') == TokenType.ACCESS_TOKEN.value:
            return payload

    @token_exception_decorator(token_type=TokenType.REFRESH_TOKEN.value, error_detail='Invalid refresh token')
    async def decode_refresh_token(self, refresh_token: str, secret_key: str, algorithm: str):
        payload: dict = jwt.decode(token=refresh_token, key=secret_key, algorithms=algorithm)
        if payload.get('token_type') != TokenType.REFRESH_TOKEN.value:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid type for token')
        return payload


class CreateTokensMixin:
    @staticmethod
    async def create_tokens(email: str, token_service: TokenServiceInterface):
        access_token = await token_service.create_token(email=email, token_type='access_token', **ACCESS_TOKEN_DATA)
        refresh_token = await token_service.create_token(email=email, token_type='refresh_token', **REFRESH_TOKEN_DATA)
        return {'access_token': access_token, 'refresh_token': refresh_token}
