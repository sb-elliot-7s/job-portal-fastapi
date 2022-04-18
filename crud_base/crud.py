from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select


class DeleteObjBase:

    @staticmethod
    async def delete_obj(column, obj_id: int, session: AsyncSession, expressions):
        res = await session.execute(delete(column).where(column.id == obj_id, expressions))
        if result := res.rowcount:
            await session.commit()
        return result


class GetObjBase:
    @staticmethod
    async def get_single_obj_or_none(column, obj_id: int, session: AsyncSession, detail: str):
        res = await session.execute(select(column).where(column.id == obj_id))
        if not (obj := res.scalars().first()):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        return obj
