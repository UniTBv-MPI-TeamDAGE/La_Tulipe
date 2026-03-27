from fastapi import FastAPI

from app.core.bootstrap import ensure_default_admin
from app.database.db import Base, engine
from app.routes import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)
ensure_default_admin()

app.include_router(auth.router)