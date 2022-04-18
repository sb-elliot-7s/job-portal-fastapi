from typing import Optional
from .interfaces.repository_interface import JobRepositoryInterface
from users.models import UserAccount
from .schemas import CreateJobSkillSchema, CreateJobSchema


class JobService:
    def __init__(self, repository: JobRepositoryInterface):
        self._repository = repository

    async def get_all_jobs(self, limit: Optional[int] = 20, offset: Optional[int] = 0):
        return await self._repository.get_all_jobs(limit=limit, offset=offset)

    async def get_jobs_from_company(self, company_id: int, limit: Optional[int] = 20, offset: Optional[int] = 0):
        return await self._repository.get_jobs_from_company(company_id=company_id, limit=limit, offset=offset)

    async def get_single_job(self, job_id: int):
        return await self._repository.get_single_job(job_id=job_id)

    async def add_job(self, job_data: CreateJobSchema, user: UserAccount, job_skill_data: Optional[list[CreateJobSkillSchema]]):
        return await self._repository.add_job(job_data=job_data.dict(exclude_none=True), user=user, job_skill_data=job_skill_data)

    async def delete_job(self, job_id: int, user: UserAccount):
        return await self._repository.delete_job(job_id=job_id, user=user)

    async def update_job(self, job_id: int, user: UserAccount, job_data: CreateJobSchema):
        return await self._repository.update_job(job_id=job_id, user=user, job_data=job_data.dict(exclude_none=True))

    async def add_job_skill(self, job_id: int, user: UserAccount, job_skill: list[CreateJobSkillSchema]):
        return await self._repository.add_job_skill(job_id=job_id, user=user, job_skill=job_skill)

    async def remove_job_skill(self, job_skill_id: int, job_id: int, user: UserAccount):
        return await self._repository.remove_job_skill(job_skill_id=job_skill_id, job_id=job_id, user=user)
