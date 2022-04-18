from fastapi import APIRouter, Depends, status, responses
from sqlalchemy.ext.asyncio import AsyncSession
from auth.token_service import TokenService
from permissions import Permissions
from users.models import UserAccount
from .schemas import CreateEducationSchema, EducationSchema
from .services import EducationService
from .repositories import EducationRepository

from database import get_session
from endpoints import Endpoint

education_router = APIRouter(prefix='/education', tags=['educations'])

seeker_permission = Permissions(token_service=TokenService())


@education_router.get(Endpoint.EDUCATION.value)
async def get_education_from_user(session: AsyncSession = Depends(get_session),
                                  user: UserAccount = Depends(seeker_permission.get_employee_user)):
    return await EducationService(repository=EducationRepository(session=session)).get_educations_from_user(user=user)


@education_router.post(Endpoint.EDUCATION.value, status_code=status.HTTP_201_CREATED, response_model=EducationSchema)
async def add_education(education_data: CreateEducationSchema,
                        session: AsyncSession = Depends(get_session),
                        user: UserAccount = Depends(seeker_permission.get_employee_user)):
    return await EducationService(repository=EducationRepository(session=session)) \
        .add_education(education_data=education_data, user=user)


@education_router.put(Endpoint.EDUCATION_ID.value, status_code=status.HTTP_200_OK, response_model=EducationSchema)
async def update_education(updated_data: CreateEducationSchema,
                           education_id: int, session: AsyncSession = Depends(get_session),
                           user: UserAccount = Depends(seeker_permission.get_employee_user)):
    result = await EducationService(repository=EducationRepository(session=session)) \
        .update_education(education_id=education_id, education_data=updated_data, user=user)
    if not result:
        return responses.ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Education not found'})
    return result

@education_router.delete(Endpoint.EDUCATION_ID.value, status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(education_id: int, session: AsyncSession = Depends(get_session),
                           user: UserAccount = Depends(seeker_permission.get_employee_user)):
    result = await EducationService(repository=EducationRepository(session=session)) \
        .delete_education(education_id=education_id, user=user)
    if not result:
        return responses.ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Education not found'})
    return {'detail': 'Education was deleted'}
