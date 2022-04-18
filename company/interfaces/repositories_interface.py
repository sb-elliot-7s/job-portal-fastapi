from abc import ABC, abstractmethod
from typing import Optional
from fastapi import UploadFile

from company.schemas import CreateSpecializationSchema
from users.models import UserAccount


class CompanyRepositoriesInterface(ABC):

    @abstractmethod
    async def get_info_company(self, company_id: int): pass

    @abstractmethod
    async def create_company(self, data: dict, specializations: Optional[list[str]], images: Optional[list[UploadFile]],
                             user: UserAccount): pass

    @abstractmethod
    async def update_company(self, company_id: int, data: dict, user: UserAccount): pass

    @abstractmethod
    async def add_image_to_company(self, company_id: int, user: UserAccount, image: UploadFile): pass

    @abstractmethod
    async def delete_image_from_company(self, image_id: int, user: UserAccount): pass

    @abstractmethod
    async def add_specialization(self, company_id: int, specializations: list[CreateSpecializationSchema]): pass

    @abstractmethod
    async def remove_specialization(self, specialization_id: int, user: UserAccount): pass

    @abstractmethod
    async def delete_company(self, company_id: int, user: UserAccount): pass
