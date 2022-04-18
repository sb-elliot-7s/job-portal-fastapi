from users.models import UserAccount
from .interfaces.repository_interface import EducationRepositoryInterface
from .schemas import CreateEducationSchema


class EducationService:
    def __init__(self, repository: EducationRepositoryInterface):
        self._repository = repository

    async def get_educations_from_user(self, user: UserAccount):
        return await self._repository.get_educations_from_user(user=user)

    async def add_education(self, education_data: CreateEducationSchema, user: UserAccount):
        return await self._repository.add_education(education_data=education_data.dict(exclude_none=True), user=user)

    async def update_education(self, education_id: int, education_data: CreateEducationSchema, user: UserAccount):
        return await self._repository.update_education(education_id=education_id,
                                                       updated_data=education_data.dict(exclude_none=True),
                                                       user=user)

    async def delete_education(self, education_id: int, user: UserAccount):
        return await self._repository.delete_education(education_id=education_id, user=user)
