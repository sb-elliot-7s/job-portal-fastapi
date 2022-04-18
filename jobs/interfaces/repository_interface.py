from abc import ABC, abstractmethod
from typing import Optional

from jobs.schemas import CreateJobSkillSchema
from users.models import UserAccount


class JobRepositoryInterface(ABC):

    @abstractmethod
    async def get_all_jobs(self, limit: Optional[int] = 20, offset: Optional[int] = 0): pass

    @abstractmethod
    async def get_jobs_from_company(self, company_id: int, limit: Optional[int] = 20, offset: Optional[int] = 0): pass

    @abstractmethod
    async def get_single_job(self, job_id: int): pass

    @abstractmethod
    async def add_job(self, job_data: dict, user: UserAccount, job_skill_data: Optional[list[CreateJobSkillSchema]]): pass

    @abstractmethod
    async def delete_job(self, job_id: int, user: UserAccount): pass

    @abstractmethod
    async def update_job(self, job_id: int, user: UserAccount, job_data: dict): pass

    @abstractmethod
    async def add_job_skill(self, job_id: int, user: UserAccount, job_skill: list[CreateJobSkillSchema]): pass

    @abstractmethod
    async def remove_job_skill(self, job_skill_id: int, job_id: int, user: UserAccount): pass
