from sqladmin import Admin, ModelView

from .db import engine
from .models import Category, Note, Status, User, UserProfile


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.full_name, User.email, User.created_at]
    column_searchable_list = [User.full_name, User.email]
    column_sortable_list = [User.id, User.full_name, User.created_at]
    column_details_exclude_list = [User.hashed_password]
    form_excluded_columns = [User.profile, User.notes]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class NoteAdmin(ModelView, model=Note):
    column_list = [
        Note.id,
        Note.title,
        Note.content,
        Note.created_at,
        Note.user_id,
        Note.category_id,
        Note.status_id,
    ]
    column_searchable_list = [Note.title, Note.content]
    column_sortable_list = [Note.id, Note.created_at]
    name = "Note"
    name_plural = "Notes"
    icon = "fa-solid fa-note-sticky"


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name]
    column_searchable_list = [Category.name]
    column_sortable_list = [Category.id, Category.name]
    form_excluded_columns = [User.notes]
    name = "Category"
    name_plural = "Categories"
    icon = "fa-solid fa-tags"


class StatusAdmin(ModelView, model=Status):
    column_list = [Status.id, Status.name]
    column_searchable_list = [Status.name]
    form_excluded_columns = [User.notes]
    name = "Status"
    name_plural = "Statuses"
    icon = "fa-solid fa-flag"


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.user_id, UserProfile.age]
    column_sortable_list = [UserProfile.id, UserProfile.age]
    name = "Profile"
    name_plural = "Profiles"
    icon = "fa-solid fa-id-card"


def init_admin(app):
    admin = Admin(app=app, engine=engine)
    admin.add_view(UserAdmin)
    admin.add_view(NoteAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(StatusAdmin)
    admin.add_view(UserProfileAdmin)
    return admin
