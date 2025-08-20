from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def create_status(
    db: AsyncSession,
    status: schemas.StatusCreate,
) -> models.Status:
    db_status = models.Status(name=status.name)
    db.add(db_status)
    await db.commit()
    await db.refresh(db_status)
    return db_status


async def get_statuses(
    db: AsyncSession,
) -> list[models.Status]:
    result = await db.execute(select(models.Status))
    return result.scalars().all()


async def delete_status(
    db: AsyncSession,
    status_id: int,
) -> models.Status | None:
    result = await db.execute(
        select(models.Status)
        .where(models.Status.id == status_id)
    )
    db_status = result.scalar_one_or_none()
    if db_status:
        await db.delete(db_status)
        await db.commit()
    return db_status
