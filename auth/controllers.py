from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from .repositories import AuthRepositories
from .schemas import CreateUserAccountSchema, CreateUserTypeSchema, Token, RefreshToken
from .services import AuthService
from .token_service import TokenService
from .password_service import PasswordService
from passlib.context import CryptContext
from endpoints import Endpoint

auth_router = APIRouter(prefix='/auth', tags=['auth'])

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@auth_router.post(Endpoint.SIGN_UP.value, status_code=status.HTTP_201_CREATED, )
async def signup(user_account: CreateUserAccountSchema, user_type: CreateUserTypeSchema,
                 session: AsyncSession = Depends(get_session)):
    return await AuthService(
        repository=AuthRepositories(session=session), token_service=TokenService(),
        password_service=PasswordService(context=password_context)).registration(user_account=user_account, user_type=user_type)


@auth_router.post(Endpoint.LOGIN.value, response_model=Token, status_code=status.HTTP_200_OK)
async def login(user_account_data: CreateUserAccountSchema = Depends(CreateUserAccountSchema.as_form),
                session: AsyncSession = Depends(get_session)):
    return await AuthService(
        repository=AuthRepositories(session=session), token_service=TokenService(),
        password_service=PasswordService(context=password_context)).login(**user_account_data.dict(exclude_none=True))


@auth_router.post(Endpoint.REFRESH_TOKEN.value, response_model=Token, status_code=status.HTTP_201_CREATED)
async def retrieve_refresh_token(refresh_token: RefreshToken, session: AsyncSession = Depends(get_session)):
    return await AuthService(repository=AuthRepositories(session=session), token_service=TokenService(),
                             password_service=PasswordService(context=password_context)) \
        .refresh_token(refresh_token=refresh_token.refresh_token)
