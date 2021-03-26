from fastapi import FastAPI

from typing import List

from .database import db

from .database import User
from .database import Movie
from .database import UserReview

from .routers import user_router
from .routers import review_router

app = FastAPI(title='Movies Review CF', 
            description='APIs for contact Apis', 
            version='0.1')

app.include_router(user_router)
app.include_router(review_router)

@app.on_event("startup")
async def startup():
    if db.is_closed():
        db.connect()
    
    db.create_tables([User, Movie, UserReview])

@app.on_event("shutdown")
async def startup():
    if not db.is_closed():
        db.close()

