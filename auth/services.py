import json

from users.models import UserAccount
from .interfaces.repositories_interface import AuthRepositoriesInterface
from .schemas import CreateUserAccountSchema, CreateUserTypeSchema, CodeFromEmailSchema
from fastapi import HTTPException, status
from .interfaces.password_interface import PasswordServiceInterface
from .interfaces.token_service_interface import TokenServiceInterface
from constants import TOKEN_DATA
from settings import get_settings
from .token_service import CreateTokensMixin
from faust_app.emails.agents import send_email_topic
from .two_factor_auth_utils import TwoFactorAuthInterface


class EmailAuthService(CreateTokensMixin):
    def __init__(self, repository: AuthRepositoriesInterface, password_service: PasswordServiceInterface, token_service: TokenServiceInterface,
                 two_factor_auth_context: TwoFactorAuthInterface = None):
        self._repository = repository
        self._password_service = password_service
        self._token_service = token_service
        self._settings = get_settings()
        self._two_factor_auth_context = two_factor_auth_context

    async def _authenticate(self, email: str, password: str):
        if not (user := await self._repository.get_user_by_email(email=email)) \
                or not await self._password_service.verify_password(plain_password=password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect username or password')
        return user

    async def registration(self, user_account: CreateUserAccountSchema, user_type: CreateUserTypeSchema):
        if await self._repository.get_user_by_email(email=user_account.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this email_agent exists')
        hash_password = await self._password_service.get_hashed_password(password=user_account.password)
        data_without_password = user_account.dict(exclude={'password'})
        return await self._repository.save_user(password=hash_password, **data_without_password, user_type_name=user_type.user_type_name)

    async def login(self, email: str, password: str):
        user = await self._authenticate(email=email, password=password)
        code = await self._two_factor_auth_context.generate_code()
        await send_email_topic.send(value=json.dumps({'email': user.email, 'code': code}).encode())
        temporary_token = await self._token_service.create_token(email=email, token_type='access_token', exp_time=3,
                                                                 algorithm=self._settings.algorithm, secret_key=self._settings.secret_key)
        return {'temporary_token': temporary_token}

    async def refresh_token(self, refresh_token: str):
        payload: dict = await self._token_service.decode_refresh_token(refresh_token=refresh_token, **TOKEN_DATA)
        return await self.create_tokens(email=payload.get('email_agent'), token_service=self._token_service)

    async def verify_code_from_email(self, code: CodeFromEmailSchema, user: UserAccount):
        code = code.code
        if not await self._two_factor_auth_context.verify_code(code):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Code not valid')
        return await self.create_tokens(email=user.email, token_service=self._token_service)
