from fastapi import FastAPI
from app.database import engine, Base
from app.api import routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes.router)
