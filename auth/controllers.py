from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from permissions import Permissions
from users.models import UserAccount
from .repositories import AuthRepositories
from .schemas import CreateUserAccountSchema, CreateUserTypeSchema, Token, RefreshToken, CodeFromEmailSchema
from .services import EmailAuthService
from .token_service import TokenService
from .password_service import PasswordService
from passlib.context import CryptContext
from endpoints import Endpoint

auth_router = APIRouter(prefix='/auth', tags=['auth'])

user_first_login = Permissions(token_service=TokenService())
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@auth_router.post(Endpoint.SIGN_UP.value, status_code=status.HTTP_201_CREATED, )
async def signup(user_account: CreateUserAccountSchema, user_type: CreateUserTypeSchema,
                 session: AsyncSession = Depends(get_session)):
    return await EmailAuthService(
        repository=AuthRepositories(session=session), token_service=TokenService(),
        password_service=PasswordService(context=password_context)).registration(user_account=user_account, user_type=user_type)


@auth_router.post(Endpoint.LOGIN.value, status_code=status.HTTP_200_OK)
async def login(user_account_data: CreateUserAccountSchema = Depends(CreateUserAccountSchema.as_form),
                session: AsyncSession = Depends(get_session)):
    return await EmailAuthService(repository=AuthRepositories(session=session), token_service=TokenService(),
                                  password_service=PasswordService(context=password_context)) \
        .login(**user_account_data.dict(exclude_none=True))


@auth_router.post('/verify_code', status_code=status.HTTP_201_CREATED, response_model=Token)
async def verify_code_from_email(code: CodeFromEmailSchema, session: AsyncSession = Depends(get_session),
                                 user: UserAccount = Depends(user_first_login.get_user_before_authorize)):
    return await EmailAuthService(repository=AuthRepositories(session=session), token_service=TokenService(),
                                  password_service=PasswordService(context=password_context)) \
        .verify_code_from_email(code=code, user=user)


@auth_router.post(Endpoint.REFRESH_TOKEN.value, response_model=Token, status_code=status.HTTP_201_CREATED)
async def retrieve_refresh_token(refresh_token: RefreshToken, session: AsyncSession = Depends(get_session)):
    return await EmailAuthService(repository=AuthRepositories(session=session), token_service=TokenService(),
                                  password_service=PasswordService(context=password_context)) \
        .refresh_token(refresh_token=refresh_token.refresh_token)
