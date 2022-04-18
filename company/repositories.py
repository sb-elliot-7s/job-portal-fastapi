from typing import Optional, Union
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from redis_service import RedisService
from settings import get_settings
from users.models import UserAccount
from .interfaces.repositories_interface import CompanyRepositoriesInterface
from .models import Company, CompanyImage, Specialization
from .schemas import CreateSpecializationSchema
from crud_base.crud import DeleteObjBase, GetObjBase


class CompanyRepository(DeleteObjBase, GetObjBase, CompanyRepositoriesInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_info_company(self, company_id: int):
        return await self.get_single_obj_or_none(column=Company, obj_id=company_id, session=self._session, detail='Company not found')

    async def _save_image(self, company_id: int, images: Optional[list[UploadFile]]):
        print(images)
        if images:
            await self._session.execute(insert(CompanyImage).values(
                [{'company_id': company_id,
                  'photo_url': get_settings().domain + f'/images/{uuid4()}/{image.filename}'} for image in images]))

    async def _save_specialization(self, company_id: int, specializations: Optional[list[Union[CreateSpecializationSchema, str]]] = None):
        if specializations:
            for spec in specializations:
                _ = await self._session.execute(
                    insert(Specialization).values(specialization_name=spec if isinstance(spec, str) else spec.specialization_name,
                                                  company_id=company_id)
                )

    async def create_company(self, data: dict, specializations: Optional[list[str]], images: Optional[list[UploadFile]], user: UserAccount):
        """created once"""
        result = await self._session.execute(insert(Company).values(**data, user_account_id=user.id))
        company_id = result.inserted_primary_key[0]
        await self._save_image(company_id=company_id, images=images)
        await self._save_specialization(company_id=company_id, specializations=specializations)
        await self._session.commit()
        a = await self._session.execute(select(Company).where(Company.id == company_id, Company.user_account_id == user.id))
        return a.scalars().first()

    async def update_company(self, company_id: int, data: dict, user: UserAccount):
        _ = await self._session.execute(update(Company)
                                        .where(Company.id == company_id, Company.user_account_id == user.id)
                                        .values(**data))
        await self._session.commit()
        company_result = await self._session.execute(select(Company).where(Company.id == company_id))
        return company_result.scalars().first()

    async def delete_company(self, company_id: int, user: UserAccount):
        return await self.delete_obj(obj_id=company_id, column=Company, session=self._session, expressions=Company.user_account_id == user.id)

    async def add_image_to_company(self, company_id: int, user: UserAccount, image: UploadFile):
        image_name = str(uuid4()) + '/' + image.filename
        # save to the cloud or local computer
        res = await self._session.execute(insert(CompanyImage)
                                          .values(company_id=company_id, photo_url=get_settings().domain + f'/images/{image_name}')
                                          .returning(CompanyImage))
        await self._session.commit()
        return res.first()

    async def delete_image_from_company(self, image_id: int, user: UserAccount):
        return await self.delete_obj(obj_id=image_id, column=CompanyImage, session=self._session,
                                     expressions=CompanyImage.company_id == user.company.id)

    async def add_specialization(self, company_id: int, specializations: list[CreateSpecializationSchema]):
        await self._save_specialization(company_id=company_id, specializations=specializations)
        await self._session.commit()
        return True

    async def remove_specialization(self, specialization_id: int, user: UserAccount):
        return await self.delete_obj(column=Specialization, session=self._session, obj_id=specialization_id,
                                     expressions=Specialization.company_id == user.company.id)
