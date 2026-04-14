from fastapi import FastAPI
from app.api.routes import router

'''
from app.db.session import engine
from app.db.base import Base
import app.db.models.user  # IMPORTANT (registers model)
'''

app = FastAPI()

'''
# Create tables on startup (TEMPORARY)
Base.metadata.create_all(bind=engine)
'''

app.include_router(router)