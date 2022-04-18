from abc import ABC, abstractmethod

from users.models import UserAccount


class EducationRepositoryInterface(ABC):

    @abstractmethod
    async def get_educations_from_user(self, user: UserAccount): pass

    @abstractmethod
    async def add_education(self, education_data: dict, user: UserAccount): pass

    @abstractmethod
    async def update_education(self, education_id: int, updated_data: dict, user: UserAccount): pass

    @abstractmethod
    async def delete_education(self, education_id: int, user: UserAccount): pass
