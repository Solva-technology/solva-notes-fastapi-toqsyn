import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.core.security import ALGORITHM, SECRET_KEY
from app.db import get_async_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_async_db)],
) -> models.User:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise cred_exc
        user_id = int(sub)
    except (JWTError, ValueError):
        raise cred_exc

    user = await db.get(models.User, user_id)
    if user is None:
        raise cred_exc
    return user


async def get_current_admin(
    current_user: Annotated[models.User, Depends(get_current_user)],
) -> models.User:
    admin_emails = {
        e.strip().lower()
        for e in os.getenv("ADMIN_EMAILS", "").split(",")
        if e.strip()
    }
    if current_user.email.lower() not in admin_emails:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user
