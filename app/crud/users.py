from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models, schemas
from app.core.security import get_password_hash


async def create_user(
    db: AsyncSession,
    user: schemas.UserCreate,
) -> models.User:
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_pw,
        created_at=datetime.utcnow(),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[models.User]:
    result = await db.execute(
        select(models.User)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> Optional[models.User]:
    result = await db.execute(
        select(models.User)
        .where(models.User.email == email)
    )
    return result.scalars().first()
