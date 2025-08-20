from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.core.depends import get_current_user
from app.core.security import (ACCESS_TOKEN_EXPIRE_MINUTES,
                               create_access_token, verify_password)
from app.crud.users import create_user, get_user_by_email
from app.db import get_async_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserOut, status_code=201)
async def register(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_async_db),
):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=400, detail="Email already registered"
        )
    user = await create_user(db, user_in)
    return user


@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserOut)
async def me(
    current_user: models.User = Depends(get_current_user),
):
    return current_user
