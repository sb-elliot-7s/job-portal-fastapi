from typing import Optional
from fastapi import UploadFile

from users.models import UserAccount
from .interfaces.repositories_interface import CompanyRepositoriesInterface
from .schemas import CreateCompanySchema, CreateSpecializationSchema


class CompanyService:
    def __init__(self, repository: CompanyRepositoriesInterface):
        self._repository = repository

    async def get_info_company(self, company_id: int):
        return await self._repository.get_info_company(company_id=company_id)

    async def create_company(self, user: UserAccount, specializations: Optional[list[str]],
                             created_company_data: CreateCompanySchema, images: Optional[list[UploadFile]]):
        return await self._repository.create_company(data=created_company_data.dict(exclude_none=True),
                                                     specializations=specializations, images=images, user=user)

    async def update_company(self, company_id: int, user: UserAccount, updated_company_data: CreateCompanySchema):
        return await self._repository.update_company(company_id=company_id, user=user,
                                                     data=updated_company_data.dict(exclude_none=True))

    async def delete_company(self, company_id: int, user: UserAccount, ):
        return await self._repository.delete_company(company_id=company_id, user=user)

    async def delete_image_from_company(self, image_id: int, user: UserAccount):
        return await self._repository.delete_image_from_company(image_id=image_id, user=user)

    async def add_image_to_company(self, company_id: int, user: UserAccount, image: UploadFile):
        return await self._repository.add_image_to_company(company_id=company_id, user=user, image=image)

    async def add_specialization(self, company_id: int, specializations: list[CreateSpecializationSchema]):
        return await self._repository.add_specialization(company_id=company_id, specializations=specializations)

    async def remove_specialization(self, specialization_id: int, user: UserAccount):
        return await self._repository.remove_specialization(specialization_id=specialization_id, user=user)
