from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def create_note(
    db: AsyncSession,
    note: schemas.NoteCreate
) -> models.Note:
    db_note = models.Note(
        title=note.title,
        content=note.content,
        category_id=note.category_id,
        status_id=note.status_id,
        user_id=note.user_id,
        created_at=datetime.utcnow(),
    )
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


async def get_notes(
    db: AsyncSession,
    skip: int = 0, limit: int = 100
) -> list[models.Note]:
    result = await db.execute(
        select(models.Note)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_note(db: AsyncSession, note_id: int) -> models.Note | None:
    result = await db.execute(
        select(models.Note)
        .where(models.Note.id == note_id)
    )
    return result.scalar_one_or_none()


async def update_note(
    db: AsyncSession,
    note_id: int, note: schemas.NoteUpdate
) -> models.Note | None:
    result = await db.execute(
        select(models.Note)
        .where(models.Note.id == note_id)
    )
    db_note = result.scalar_one_or_none()
    if not db_note:
        return None

    for field, value in note.dict(exclude_unset=True).items():
        setattr(db_note, field, value)

    await db.commit()
    await db.refresh(db_note)
    return db_note


async def delete_note(db: AsyncSession, note_id: int) -> models.Note | None:
    result = await db.execute(
        select(models.Note)
        .where(models.Note.id == note_id)
    )
    db_note = result.scalar_one_or_none()
    if db_note:
        await db.delete(db_note)
        await db.commit()
    return db_note
