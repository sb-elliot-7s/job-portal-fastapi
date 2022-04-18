from sqlalchemy import insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import UserAccount
from .interfaces.repository_interface import EducationRepositoryInterface
from .models import Education
from crud_base.crud import DeleteObjBase


class EducationRepository(DeleteObjBase, EducationRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_educations_from_user(self, user: UserAccount):
        result = await self._session.execute(select(Education).where(Education.user_account_id == user.id))
        return result.scalars().all()

    async def add_education(self, education_data: dict, user: UserAccount):
        result = await self._session.execute(
            insert(Education).values(**education_data, user_account_id=user.id).returning(Education))
        await self._session.commit()
        return result.first()

    async def update_education(self, education_id: int, updated_data: dict, user: UserAccount):
        result = await self._session.execute(update(Education)
                                             .where(Education.id == education_id, Education.user_account_id == user.id)
                                             .values(**updated_data).returning(Education))
        if not result.rowcount:
            return result.rowcount
        await self._session.commit()
        return result.first()

    async def delete_education(self, education_id: int, user: UserAccount):
        return await self.delete_obj(obj_id=education_id, column=Education, session=self._session, expressions=Education.user_account_id == user.id)
