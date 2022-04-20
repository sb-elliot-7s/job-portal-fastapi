from abc import ABC, abstractmethod
from typing import Optional
from fastapi import UploadFile
from users.models import UserAccount
from users.schemas import CreateUserSkillSchema


class ProfileRepositoryInterface(ABC):

    @abstractmethod
    async def get_profile(self, user: UserAccount): pass

    @abstractmethod
    async def update_profile(self, user: UserAccount, profile_data: dict, image_name: Optional[str] = None): pass

    @abstractmethod
    async def add_experience(self, user: UserAccount, experience_data: dict): pass

    @abstractmethod
    async def update_experience(self, experience_id: int, user: UserAccount, experience_data: dict): pass

    @abstractmethod
    async def delete_experience(self, experience_id: int, user: UserAccount): pass

    @abstractmethod
    async def delete_profile(self, user: UserAccount): pass

    @abstractmethod
    async def get_all_skills(self, user: UserAccount): pass

    @abstractmethod
    async def add_skill(self, user: UserAccount, skills: list[CreateUserSkillSchema]): pass

    @abstractmethod
    async def remove_skill(self, skill_id: int, user: UserAccount): pass
