from typing import Optional
from fastapi import APIRouter, Depends, File, UploadFile, status, Form, responses
from sqlalchemy.ext.asyncio import AsyncSession
from auth.token_service import TokenService
from database import get_session
from permissions import Permissions
from users.models import UserAccount
from .repositories import CompanyRepository
from .schemas import CreateCompanySchema, CompanySchema, CompanyImageSchema, CreateSpecializationSchema
from .services import CompanyService
from endpoints import Endpoint

company_router = APIRouter(prefix='/company', tags=['companies'])

recruiter_permission = Permissions(token_service=TokenService())


@company_router.get(Endpoint.COMPANY_ID.value, status_code=status.HTTP_200_OK, response_model=CompanySchema)
async def get_info_company(company_id: int, session: AsyncSession = Depends(get_session)):
    return await CompanyService(repository=CompanyRepository(session=session)).get_info_company(company_id=company_id)


@company_router.post('/', status_code=status.HTTP_201_CREATED, response_model=CompanySchema)
async def create_company(specializations: Optional[list[str]] = Form(None),
                         company_data: CreateCompanySchema = Depends(CreateCompanySchema.as_form),
                         images: Optional[list[UploadFile]] = File(None),
                         session: AsyncSession = Depends(get_session),
                         user: UserAccount = Depends(recruiter_permission.get_recruiter_user)):
    return await CompanyService(repository=CompanyRepository(session=session)) \
        .create_company(created_company_data=company_data, images=images, user=user, specializations=specializations)


@company_router.put(Endpoint.COMPANY_ID.value, status_code=status.HTTP_200_OK, response_model=CompanySchema)
async def update_company(company_id: int, update_data: CreateCompanySchema,
                         session: AsyncSession = Depends(get_session),
                         user: UserAccount = Depends(recruiter_permission.get_recruiter_user)):
    return await CompanyService(repository=CompanyRepository(session=session)) \
        .update_company(company_id=company_id, updated_company_data=update_data, user=user)


@company_router.delete(Endpoint.COMPANY_ID.value, status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, session: AsyncSession = Depends(get_session),
                         user: UserAccount = Depends(recruiter_permission.get_recruiter_user)):
    result = await CompanyService(repository=CompanyRepository(session=session)) \
        .delete_company(company_id=company_id, user=user)
    if not result:
        return responses.ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Company not found'})
    return {'detail': 'Company has been deleted'}


@company_router.post(Endpoint.ADD_IMAGE.value, status_code=status.HTTP_201_CREATED, response_model=CompanyImageSchema)
async def add_image(user: UserAccount = Depends(recruiter_permission.get_recruiter_user),
                    session: AsyncSession = Depends(get_session), image: UploadFile = File(...)):
    return await CompanyService(repository=CompanyRepository(session=session)).add_image_to_company(
        company_id=user.company.id, user=user, image=image)


@company_router.delete(Endpoint.IMAGES_ID.value, status_code=status.HTTP_204_NO_CONTENT)
async def delete_image_from_company(image_id: int, user: UserAccount = Depends(recruiter_permission.get_recruiter_user),
                                    session: AsyncSession = Depends(get_session)):
    result = await CompanyService(repository=CompanyRepository(session=session)) \
        .delete_image_from_company(image_id=image_id, user=user)
    if not result:
        return responses.ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Image not found'})
    return {'detail': 'Image has been deleted'}


@company_router.post(Endpoint.SPECIALIZATIONS.value, status_code=status.HTTP_201_CREATED)
async def add_specialization(specializations: list[CreateSpecializationSchema],
                             user: UserAccount = Depends(recruiter_permission.get_recruiter_user),
                             session: AsyncSession = Depends(get_session)):
    result = await CompanyService(repository=CompanyRepository(session=session)) \
        .add_specialization(company_id=user.company.id, specializations=specializations)
    if result:
        return {'detail': 'Specialization has been added'}


@company_router.delete(Endpoint.SPECIALIZATION_ID.value, status_code=status.HTTP_204_NO_CONTENT)
async def remove_specialization(specialization_id: int, user: UserAccount = Depends(recruiter_permission.get_recruiter_user),
                                session: AsyncSession = Depends(get_session)):
    result = await CompanyService(repository=CompanyRepository(session=session)) \
        .remove_specialization(specialization_id=specialization_id, user=user)
    if not result:
        return responses.ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Specialization not found'})
    return {'detail': 'Specialization has been deleted'}
