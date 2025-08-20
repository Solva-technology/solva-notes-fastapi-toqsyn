from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow,
    )
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    profile: Mapped["UserProfile"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    notes: Mapped[list["Note"]] = relationship(back_populates="user")

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return f"<User id={self.id} name={self.full_name} email={self.email}>"


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    user: Mapped["User"] = relationship(back_populates="profile")

    def __str__(self):
        return f"Profile {self.id}"

    def __repr__(self):
        return (
            f"<UserProfile id={self.id} user_id={self.user_id} "
            f"age={self.age}>"
        )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    notes: Mapped[list["Note"]] = relationship(back_populates="category")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"


class Status(Base):
    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    notes: Mapped[list["Note"]] = relationship(back_populates="status")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Status id={self.id} name={self.name}>"


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False,
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"), nullable=True,
    )
    status_id: Mapped[int | None] = mapped_column(
        ForeignKey("statuses.id"), nullable=True,
    )
    user: Mapped["User"] = relationship(back_populates="notes")
    category: Mapped["Category"] = relationship(back_populates="notes")
    status: Mapped["Status"] = relationship(back_populates="notes")

    def __str__(self) -> str:
        return (
            f"{self.title} "
            f"(by {self.user.full_name if self.user else 'Unknown'})"
        )

    def __repr__(self) -> str:
        return (
            f"<Note id={self.id} title={self.title!r} "
            f"user_id={self.user_id}"
            f"category_id={self.category_id}"
            f"status_id={self.status_id}>"
        )
