from typing import Optional
from fastapi import APIRouter, Depends, status, responses
from sqlalchemy.ext.asyncio import AsyncSession
from auth.token_service import TokenService
from database import get_session
from permissions import Permissions
from users.models import UserAccount
from .schemas import CreateJobSkillSchema, CreateJobSchema, JobSchema
from .services import JobService
from .repositories import JobRepository
from endpoints import Endpoint

jobs_router = APIRouter(prefix='/jobs', tags=['jobs'])
recruiter_permissions = Permissions(token_service=TokenService())


@jobs_router.delete(Endpoint.JOB_ID.value, status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: int, session: AsyncSession = Depends(get_session),
                     user: UserAccount = Depends(recruiter_permissions.get_recruiter_user)):
    if not (_ := await JobService(repository=JobRepository(session=session)).delete_job(job_id=job_id, user=user)):
        return responses.ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Job not found'})
    return {'detail': 'Job has been deleted'}


@jobs_router.get(Endpoint.COMPANY_COMPANY_ID.value, status_code=status.HTTP_200_OK, response_model=list[JobSchema])
async def get_all_jobs_from_company(company_id: int, limit: Optional[int] = 20, offset: Optional[int] = 0,
                                    session: AsyncSession = Depends(get_session)):
    return await JobService(repository=JobRepository(session=session)) \
        .get_jobs_from_company(company_id=company_id, limit=limit, offset=offset)


@jobs_router.get(Endpoint.JOB_ID.value, status_code=status.HTTP_200_OK, response_model=JobSchema)
async def get_single_job(job_id: int, session: AsyncSession = Depends(get_session)):
    return await JobService(repository=JobRepository(session=session)).get_single_job(job_id=job_id)


@jobs_router.post(Endpoint.JOB.value, status_code=status.HTTP_201_CREATED, response_model=JobSchema)
async def add_job(job: CreateJobSchema, job_skill: Optional[list[CreateJobSkillSchema]],
                  session: AsyncSession = Depends(get_session),
                  user: UserAccount = Depends(recruiter_permissions.get_recruiter_user)):
    return await JobService(repository=JobRepository(session=session)) \
        .add_job(job_data=job, user=user, job_skill_data=job_skill)


@jobs_router.put(Endpoint.JOB_ID.value, status_code=status.HTTP_200_OK)
async def update_job(job_id: int, job_data: CreateJobSchema, session: AsyncSession = Depends(get_session),
                     user: UserAccount = Depends(recruiter_permissions.get_recruiter_user)):
    return await JobService(repository=JobRepository(session=session)).update_job(job_id=job_id, user=user, job_data=job_data)


@jobs_router.get(Endpoint.JOB.value, status_code=status.HTTP_200_OK, response_model=list[JobSchema])
async def get_all_jobs(limit: Optional[int] = 20, offset: Optional[int] = 0, session: AsyncSession = Depends(get_session)):
    return await JobService(repository=JobRepository(session=session)).get_all_jobs(limit=limit, offset=offset)


@jobs_router.post(Endpoint.JOB_SKILL_TO_JOB_ID.value, status_code=status.HTTP_201_CREATED)
async def add_job_skill(job_id: int, job_skill: list[CreateJobSkillSchema], session: AsyncSession = Depends(get_session),
                        user: UserAccount = Depends(recruiter_permissions.get_recruiter_user)):
    if not (_ := await JobService(repository=JobRepository(session=session)).add_job_skill(job_id=job_id, user=user, job_skill=job_skill)):
        return responses.ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'Empty list'})
    return {'detail': 'Job skill has been added'}


@jobs_router.delete(Endpoint.JOB_SKILL_ID.value + '/{job_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_job_skill(skill_id: int, job_id: int, session: AsyncSession = Depends(get_session),
                           user: UserAccount = Depends(recruiter_permissions.get_recruiter_user)):
    if not (_ := await JobService(repository=JobRepository(session=session)).remove_job_skill(job_skill_id=skill_id, job_id=job_id, user=user)):
        return responses.ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': 'Job skill not found'})
    return {'detail': 'Job skill has been deleted'}
