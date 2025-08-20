from fastapi import FastAPI

from app.admin import init_admin
from app.routers import auth, categories, notes, status, users

app = FastAPI(title="Note App")

init_admin(app)

app.include_router(users.router)
app.include_router(notes.router)
app.include_router(categories.router)
app.include_router(status.router)
app.include_router(auth.router)
