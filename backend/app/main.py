from fastapi import FastAPI

from app.database.db import Base, engine
from app.routes import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)