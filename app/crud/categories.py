from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def create_category(
    db: AsyncSession,
    category: schemas.CategoryCreate,
) -> models.Category:
    db_category = models.Category(name=category.name)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def get_categories(db: AsyncSession) -> list[models.Category]:
    result = await db.execute(models.Category.__table__.select())
    return result.scalars().all()


async def delete_category(
    db: AsyncSession,
    category_id: int,
) -> models.Category | None:
    result = await db.execute(
        models.Category.__table__.select()
        .where(models.Category.id == category_id)
    )
    db_category = result.scalar_one_or_none()
    if db_category:
        await db.delete(db_category)
        await db.commit()
    return db_category
