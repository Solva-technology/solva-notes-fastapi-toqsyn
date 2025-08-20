from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    full_name: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None
    category_id: Optional[int] = None
    status_id: Optional[int] = None


class NoteCreate(NoteBase):
    user_id: int


class NoteOut(NoteBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    status_id: Optional[int] = None


class StatusBase(BaseModel):
    name: str


class StatusCreate(StatusBase):
    pass


class StatusOut(StatusBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
