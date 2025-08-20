from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.db import get_async_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserOut)
async def create_user(
    user: schemas.UserCreate,
    database: AsyncSession = Depends(get_async_db),
):
    return await crud.users.create_user(database, user)


@router.get("/", response_model=list[schemas.UserOut])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    database: AsyncSession = Depends(get_async_db),
):
    return await crud.users.get_users(database, skip=skip, limit=limit)
