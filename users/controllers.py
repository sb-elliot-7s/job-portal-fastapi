from typing import Optional
from fastapi import APIRouter, Depends, status, File, UploadFile, responses
from sqlalchemy.ext.asyncio import AsyncSession
from auth.token_service import TokenService
from database import get_session
from permissions import Permissions
from .repositories import ProfileRepository
from .services import ProfileService
from .schemas import CreateProfileSchema, CreateExperienceSchema, ProfileSchema, CreateUserSkillSchema, ExperienceSchema, \
    UserSkillSchema
from .models import UserAccount
from endpoints import Endpoint

profile_router = APIRouter(prefix='/users', tags=['users'])

seeker_permission = Permissions(token_service=TokenService())


@profile_router.post(Endpoint.EXPERIENCE.value, status_code=status.HTTP_201_CREATED, response_model=ExperienceSchema)
async def add_experience(experience_data: CreateExperienceSchema,
                         user: UserAccount = Depends(seeker_permission.get_employee_user),
                         session: AsyncSession = Depends(get_session)):
    return await ProfileService(repository=ProfileRepository(session=session)).add_experience(user=user, experience_data=experience_data)


@profile_router.put(Endpoint.EXPERIENCE_ID.value, status_code=status.HTTP_200_OK, response_model=ExperienceSchema)
async def update_experience(experience_id: int, experience_data: CreateExperienceSchema,
                            user: UserAccount = Depends(seeker_permission.get_employee_user),
                            session: AsyncSession = Depends(get_session)):
    return await ProfileService(repository=ProfileRepository(session=session)) \
        .update_experience(experience_id=experience_id, user=user, experience_data=experience_data)


@profile_router.delete(Endpoint.EXPERIENCE_ID.value, status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(experience_id: int, user: UserAccount = Depends(seeker_permission.get_employee_user),
                            session: AsyncSession = Depends(get_session)):
    result = await ProfileService(repository=ProfileRepository(session=session)).delete_experience(experience_id=experience_id, user=user)
    if not result:
        return responses.ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Experience not found'})
    return {'detail': 'Experience has been deleted'}


@profile_router.get(Endpoint.PROFILE.value, status_code=status.HTTP_200_OK, response_model=ProfileSchema)
async def get_user_profile(user: UserAccount = Depends(seeker_permission.get_employee_user),
                           session: AsyncSession = Depends(get_session)):
    return await ProfileService(repository=ProfileRepository(session=session)).get_profile(user=user)


@profile_router.put(Endpoint.PROFILE.value, status_code=status.HTTP_200_OK)
async def update_profile(profile_data: CreateProfileSchema = Depends(CreateProfileSchema.as_form),
                         image: Optional[UploadFile] = File(None),
                         user: UserAccount = Depends(seeker_permission.get_employee_user),
                         session: AsyncSession = Depends(get_session)):
    return await ProfileService(repository=ProfileRepository(session=session)) \
        .update_profile(user=user, profile_data=profile_data, image=image)


@profile_router.delete(Endpoint.PROFILE.value, status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(user: UserAccount = Depends(seeker_permission.get_employee_user),
                         session: AsyncSession = Depends(get_session)):
    result = await ProfileService(repository=ProfileRepository(session=session)).delete_profile(user=user)
    if not result:
        return responses.ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'User not found'})
    return {'detail': 'User has been deleted'}


@profile_router.get(Endpoint.SKILLS.value, status_code=status.HTTP_200_OK, response_model=list[UserSkillSchema])
async def get_all_skills(user: UserAccount = Depends(seeker_permission.get_employee_user), session: AsyncSession = Depends(get_session)):
    return await ProfileService(repository=ProfileRepository(session=session)).get_all_skills(user=user)


@profile_router.post(Endpoint.SKILLS.value, status_code=status.HTTP_201_CREATED, response_model=list[UserSkillSchema])
async def add_skills(skills: list[CreateUserSkillSchema], user: UserAccount = Depends(seeker_permission.get_employee_user),
                     session: AsyncSession = Depends(get_session)):
    return await ProfileService(repository=ProfileRepository(session=session)).add_skill(user=user, skills=skills)


@profile_router.delete(Endpoint.SKILL_ID.value, status_code=status.HTTP_204_NO_CONTENT)
async def remove_skill(skill_id: int, user: UserAccount = Depends(seeker_permission.get_employee_user),
                       session: AsyncSession = Depends(get_session)):
    result = await ProfileService(repository=ProfileRepository(session=session)).remove_skill(skill_id=skill_id, user=user)
    if not result:
        return responses.ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Skill not found'})
    return {'detail': 'Skill has been deleted'}
