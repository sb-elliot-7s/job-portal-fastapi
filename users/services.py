from typing import Optional

from fastapi import UploadFile, File

from .interfaces.repositories_interface import ProfileRepositoryInterface
from .models import UserAccount
from .schemas import CreateExperienceSchema, CreateProfileSchema, CreateUserSkillSchema


class ProfileService:
    def __init__(self, repository: ProfileRepositoryInterface):
        self._repository = repository

    async def get_profile(self, user: UserAccount):
        return await self._repository.get_profile(user=user)

    async def delete_profile(self, user: UserAccount):
        return await self._repository.delete_profile(user=user)

    async def update_profile(self, user: UserAccount, profile_data: CreateProfileSchema,
                             image: Optional[UploadFile] = File(None)):
        return await self._repository.update_profile(user=user, image=image, profile_data=profile_data.dict(exclude_none=True))

    async def add_experience(self, user: UserAccount, experience_data: CreateExperienceSchema):
        return await self._repository.add_experience(user=user, experience_data=experience_data.dict(exclude_none=True))

    async def update_experience(self, experience_id: int, user: UserAccount, experience_data: CreateExperienceSchema):
        return await self._repository \
            .update_experience(experience_id=experience_id, user=user, experience_data=experience_data.dict(exclude_none=True))

    async def delete_experience(self, experience_id: int, user: UserAccount):
        return await self._repository.delete_experience(experience_id=experience_id, user=user)

    async def get_all_skills(self, user: UserAccount):
        return await self._repository.get_all_skills(user=user)

    async def add_skill(self, user: UserAccount, skills: list[CreateUserSkillSchema]):
        return await self._repository.add_skill(user=user, skills=skills)

    async def remove_skill(self, user: UserAccount, skill_id: int):
        return await self._repository.remove_skill(skill_id=skill_id, user=user)
