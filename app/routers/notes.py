from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.core.depends import get_current_user
from app.db import get_async_db

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=schemas.NoteOut)
async def create_note(
    note: schemas.NoteCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user),
):
    category_result = await db.execute(
        select(models.Category).where(models.Category.id == note.category_id)
    )
    category = category_result.scalar_one_or_none()
    if not category:
        raise HTTPException(
            status_code=400, detail="Category does not exist"
        )

    db_note = models.Note(
        title=note.title,
        content=note.content,
        category_id=note.category_id,
        user_id=current_user.id,
    )
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


@router.get("/", response_model=list[schemas.NoteOut])
async def read_notes(
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.is_admin:
        result = await db.execute(select(models.Note))
    else:
        result = await db.execute(
            select(models.Note).where(models.Note.user_id == current_user.id)
        )
    return result.scalars().all()


@router.get("/{note_id}", response_model=schemas.NoteOut)
async def read_note(
    note_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(
        select(models.Note).where(models.Note.id == note_id)
    )
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if not current_user.is_admin and note.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this note"
        )

    return note


@router.put("/{note_id}", response_model=schemas.NoteOut)
async def update_note(
    note_id: int,
    updated_note: schemas.NoteCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(
        select(models.Note).where(models.Note.id == note_id)
    )
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if not current_user.is_admin and note.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this note"
        )

    category_result = await db.execute(
        select(models.Category)
        .where(models.Category.id == updated_note.category_id)
    )
    if not category_result.scalar_one_or_none():
        raise HTTPException(
            status_code=400, detail="Category does not exist"
        )

    note.title = updated_note.title
    note.content = updated_note.content
    note.category_id = updated_note.category_id

    await db.commit()
    await db.refresh(note)
    return note


@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(
        select(models.Note).where(models.Note.id == note_id)
    )
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if not current_user.is_admin and note.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this note"
        )

    await db.delete(note)
    await db.commit()
    return {"message": "Note deleted"}
