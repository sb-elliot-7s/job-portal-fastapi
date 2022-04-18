from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session

social_router = APIRouter(prefix='/social_auth', tags=['social auth'])


@social_router.post('/google')
async def login_with_google(session: AsyncSession = Depends(get_session)):
    return {}
