from users.models import UserAccount
from .interfaces.repositories_interface import AuthRepositoriesInterface
from .schemas import CreateUserAccountSchema, CreateUserTypeSchema, CodeFromEmailSchema
from fastapi import HTTPException, status
from .interfaces.password_interface import PasswordServiceInterface
from .interfaces.token_service_interface import TokenServiceInterface
from constants import ACCESS_TOKEN_DATA, REFRESH_TOKEN_DATA, TOKEN_DATA
from auth.tasks import send_code_email
from settings import get_settings
from .two_factor_auth_utils import TwoFactorAuth


class EmailAuthUtils:
    def __init__(self, repo, password_service):
        self._repo = repo
        self._password_service = password_service


class EmailAuthService:
    def __init__(self, repository: AuthRepositoriesInterface, password_service: PasswordServiceInterface, token_service: TokenServiceInterface):
        self._repository = repository
        self._password_service = password_service
        self._token_service = token_service
        self._settings = get_settings()
        self.two_factor_auth = TwoFactorAuth()

    async def _authenticate(self, email: str, password: str):
        if not (user := await self._repository.get_user_by_email(email=email)) \
                or not await self._password_service.verify_password(plain_password=password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect username or password')
        return user

    async def registration(self, user_account: CreateUserAccountSchema, user_type: CreateUserTypeSchema):
        if await self._repository.get_user_by_email(email=user_account.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this email exists')
        hash_password = await self._password_service.get_hashed_password(password=user_account.password)
        data_without_password = user_account.dict(exclude={'password'})
        return await self._repository.save_user(password=hash_password, **data_without_password, user_type_name=user_type.user_type_name)

    async def _create_tokens(self, email: str):
        access_token = await self._token_service.create_token(email=email, token_type='access_token', **ACCESS_TOKEN_DATA)
        refresh_token = await self._token_service.create_token(email=email, token_type='refresh_token', **REFRESH_TOKEN_DATA)
        return {'access_token': access_token, 'refresh_token': refresh_token}

    async def login(self, email: str, password: str):
        user = await self._authenticate(email=email, password=password)
        code = await self.two_factor_auth.generate_code()
        sender = self._settings.sender
        send_code_email.delay(sender, user.email, code)
        temporary_token = await self._token_service.create_token(email=email, token_type='access_token', exp_time=3,
                                                                 algorithm=self._settings.algorithm, secret_key=self._settings.secret_key)
        return {'temporary_token': temporary_token}

    async def refresh_token(self, refresh_token: str):
        payload: dict = await self._token_service.decode_refresh_token(refresh_token=refresh_token, **TOKEN_DATA)
        return await self._create_tokens(email=payload.get('email'))

    async def verify_code_from_email(self, code: CodeFromEmailSchema, user: UserAccount):
        code = code.code
        if not await self.two_factor_auth.verify_code(code):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Code not valid')
        return await self._create_tokens(email=user.email)
