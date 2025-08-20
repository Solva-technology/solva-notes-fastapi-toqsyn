from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.core.depends import get_current_admin, get_current_user
from app.db import get_async_db

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=schemas.CategoryOut)
async def create_category(
    category: schemas.CategoryCreate,
    db: AsyncSession = Depends(get_async_db),
    _: models.User = Depends(get_current_admin),
):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


@router.get("/", response_model=list[schemas.CategoryOut])
async def read_categories(
    db: AsyncSession = Depends(get_async_db),
    _: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.Category))
    return result.scalars().all()


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_async_db),
    _: models.User = Depends(get_current_admin),
):
    result = await db.execute(
        select(models.Category)
        .where(models.Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(
            status_code=404, detail="Category not found"
        )

    await db.delete(category)
    await db.commit()
    return {"message": "Category deleted successfully"}
