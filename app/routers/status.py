from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.core.depends import get_current_admin, get_current_user
from app.db import get_async_db

router = APIRouter(prefix="/statuses", tags=["Statuses"])


@router.post("/", response_model=schemas.StatusOut)
async def create_status(
    status: schemas.StatusCreate,
    db: AsyncSession = Depends(get_async_db),
    _: models.User = Depends(get_current_admin),
):
    db_status = models.Status(**status.dict())
    db.add(db_status)
    await db.commit()
    await db.refresh(db_status)
    return db_status


@router.get("/", response_model=list[schemas.StatusOut])
async def read_statuses(
    db: AsyncSession = Depends(get_async_db),
    _: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.Status))
    return result.scalars().all()


@router.delete("/{status_id}")
async def delete_status(
    status_id: int,
    db: AsyncSession = Depends(get_async_db),
    _: models.User = Depends(get_current_admin),
):
    result = await db.execute(
        select(models.Status).where(models.Status.id == status_id)
    )
    status = result.scalar_one_or_none()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    await db.delete(status)
    await db.commit()
    return {"message": "Status deleted"}
