from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from settings import get_settings
from sqlalchemy import select
from auth.interfaces.token_service_interface import TokenServiceInterface
from constants import TOKEN_DATA
from users.models import UserAccount, UserType


class Permissions:
    OAUTH_TOKEN = OAuth2PasswordBearer(tokenUrl='/login')

    def __init__(self, token_service: TokenServiceInterface):
        self._token_service = token_service
        self._settings = get_settings()

    async def _decode_token(self, token: str):
        payload: dict = await self._token_service.decode_access_token(access_token=token, **TOKEN_DATA)
        return payload.get('sub')

    async def _get_user(self, role: str, token: str, session: AsyncSession):
        email = await self._decode_token(token=token)
        user_type_id_subquery = select(UserType.id).where(UserType.user_type_value == role).scalar_subquery()
        result = await session.execute(select(UserAccount).where(UserAccount.email == email, UserAccount.is_active,
                                                                 UserAccount.user_type_id == user_type_id_subquery))
        if not (user := result.scalars().first()):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return user

    async def get_employee_user(self, token: str = Depends(OAUTH_TOKEN), session: AsyncSession = Depends(get_session)):
        return await self._get_user(role='EMPLOYEE', token=token, session=session)

    async def get_recruiter_user(self, token: str = Depends(OAUTH_TOKEN), session: AsyncSession = Depends(get_session)):
        return await self._get_user(role='RECRUITER', token=token, session=session)

    async def get_user_before_authorize(self, token: str = Depends(OAUTH_TOKEN), session: AsyncSession = Depends(get_session)):
        email = await self._decode_token(token=token)
        result = await session.execute(select(UserAccount).where(UserAccount.email == email, UserAccount.is_active))
        if not (user := result.scalars().first()):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return user
