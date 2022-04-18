from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from .interfaces.repositories_interface import AuthRepositoriesInterface
from sqlalchemy import select, insert
from users.models import UserAccount, UserType


class AuthRepositories(AuthRepositoriesInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_email(self, email: str):
        result: AsyncResult = await self._session.execute(select(UserAccount).where(UserAccount.email == email))
        return result.scalars().first()

    async def save_user(self, email: str, password: str, username: Optional[str], user_type_name: str) -> UserAccount:
        user_type_subquery = select(UserType.id).where(UserType.user_type_value == user_type_name).scalar_subquery()
        res = await self._session.execute(insert(UserAccount).values(email=email, username=username, password=password,
                                                                     user_type_id=user_type_subquery).returning(UserAccount))
        await self._session.commit()
        return res.first()
