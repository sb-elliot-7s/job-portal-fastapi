from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import UserAccount
from .interfaces.repository_interface import JobRepositoryInterface
from .models import Job, JobSkillSet
from .schemas import CreateJobSkillSchema
from crud_base.crud import DeleteObjBase, GetObjBase


class JobRepository(DeleteObjBase, GetObjBase, JobRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_jobs(self, limit: Optional[int] = 20, offset: Optional[int] = 0):
        res = await self._session.execute(select(Job).limit(limit).offset(offset).order_by(Job.created_date.desc()))
        return res.scalars().unique().all()

    async def get_jobs_from_company(self, company_id: int, limit: Optional[int] = 20, offset: Optional[int] = 0):
        res = await self._session.execute(
            select(Job).where(Job.company_id == company_id).limit(limit).offset(offset).order_by(Job.created_date.desc()))
        return res.scalars().unique().all()

    async def get_single_job(self, job_id: int):
        return await self.get_single_obj_or_none(column=Job, obj_id=job_id, session=self._session, detail='Job not found')

    async def _save_job_skills(self, job_id: int, job_skills: Optional[list[CreateJobSkillSchema]], user: UserAccount):
        if job_skills:
            job_result = await self._session.execute(select(Job).where(Job.id == job_id))
            if (job := job_result.scalars().first()) and job.company_id != user.company.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You are not added skill for this job')
            await self._session.execute(insert(JobSkillSet).values(
                [{'skill_name': skill.skill_name, 'job_id': job_id, 'company_id': user.company.id} for skill in job_skills]))
            return True
        return False

    async def add_job(self, job_data: dict, user: UserAccount, job_skill_data: Optional[list[CreateJobSkillSchema]]):
        res = await self._session.execute(insert(Job)
                                          .values(**job_data, posted_by_id=user.id, company_id=user.company.id))
        job_id = res.inserted_primary_key[0]
        await self._save_job_skills(job_id=job_id, job_skills=job_skill_data, user=user)
        await self._session.commit()
        job_result = await self._session.execute(select(Job).where(Job.id == job_id))
        return job_result.scalars().first()

    async def delete_job(self, job_id: int, user: UserAccount):
        return await self.delete_obj(obj_id=job_id, column=Job, session=self._session, expressions=Job.company_id == user.company.id)

    async def update_job(self, job_id: int, user: UserAccount, job_data: dict):
        res = await self._session.execute(update(Job)
                                          .where(Job.id == job_id, Job.company_id == user.company.id)
                                          .values(**job_data)
                                          .returning(Job))
        await self._session.commit()
        return res.first()

    async def add_job_skill(self, job_id: int, user: UserAccount, job_skill: list[CreateJobSkillSchema]):
        if result := await self._save_job_skills(job_id=job_id, job_skills=job_skill, user=user):
            await self._session.commit()
        return result

    async def remove_job_skill(self, job_skill_id: int, job_id: int, user: UserAccount):
        stmt = delete(JobSkillSet).where(JobSkillSet.id == job_skill_id, JobSkillSet.job_id == job_id, JobSkillSet.company_id == user.company.id)
        r = await self._session.execute(stmt)
        if result := r.rowcount:
            await self._session.commit()
        return result
