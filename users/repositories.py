from typing import Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .interfaces.repositories_interface import ProfileRepositoryInterface
from .models import UserAccount, Experience, UserSkill
from settings import get_settings
from .schemas import CreateUserSkillSchema
from crud_base.crud import DeleteObjBase, GetObjBase


class ProfileRepository(DeleteObjBase, GetObjBase, ProfileRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_profile(self, user: UserAccount):
        return await self.get_single_obj_or_none(column=UserAccount, session=self._session, obj_id=user.id, detail='User not found')

    async def update_profile(self, user: UserAccount, profile_data: dict, image_name: Optional[str] = None):
        stmt = update(UserAccount).values(**profile_data).where(UserAccount.id == user.id)
        if image_name:
            stmt = stmt.values(user_image_url=get_settings().domain + f'/images/{image_name}')
        profile_res = await self._session.execute(stmt.returning(UserAccount))
        await self._session.commit()
        return profile_res.first()

    async def add_experience(self, user: UserAccount, experience_data: dict):
        res = await self._session.execute(insert(Experience).values(**experience_data, user_account_id=user.id).returning(Experience))
        await self._session.commit()
        return res.first()

    async def update_experience(self, experience_id: int, user: UserAccount, experience_data: dict):
        res = await self._session.execute(update(Experience)
                                          .where(Experience.id == experience_id, Experience.user_account_id == user.id)
                                          .values(**experience_data)
                                          .returning(Experience))
        await self._session.commit()
        return res.first()

    async def delete_experience(self, experience_id: int, user: UserAccount):
        return await self.delete_obj(obj_id=experience_id, column=Experience, session=self._session,
                                     expressions=Experience.user_account_id == user.id)

    async def delete_profile(self, user: UserAccount):
        res = await self._session.execute(delete(UserAccount).where(UserAccount.id == user.id))
        if result := res:
            await self._session.commit()
        return result

    async def get_all_skills(self, user: UserAccount):
        res = await self._session.execute(select(UserSkill).where(UserSkill.user_account_id == user.id))
        return res.scalars().all()

    async def add_skill(self, user: UserAccount, skills: list[CreateUserSkillSchema]):
        res = await self._session.execute(insert(UserSkill)
                                          .values([{'skill_name': skill.skill_name, 'user_account_id': user.id} for skill in skills])
                                          .returning(UserSkill))
        await self._session.commit()
        return res.all()

    async def remove_skill(self, skill_id: int, user: UserAccount):
        return await self.delete_obj(obj_id=skill_id, column=UserSkill, session=self._session, expressions=UserSkill.user_account_id == user.id)
