from fastapi import FastAPI

from .database import db

from .database import User
from .database import Movie
from .database import UserReview

from .schemas import UserRequestModel
from .schemas import UserResponseModel

from .schemas import UserReviewBaseModel

from .schemas import UserReviewRequestModel
from .schemas import UserReviewResponseModel

app = FastAPI(title='Movies Review CF', 
            description='APIs for contact Apis', 
            version='0.1')

@app.on_event("startup")
async def startup():
    if db.is_closed():
        db.connect()
    
    db.create_tables([User, Movie, UserReview])

@app.on_event("shutdown")
async def startup():
    if not db.is_closed():
        db.close()

@app.post("/users", response_model=UserResponseModel)
async def root(user: UserRequestModel):
    password = User.create_password(user.password)

    user = User.create(
        username=user.username, 
        password=password
    )

    return user

@app.post("/users/login", response_model=UserResponseModel)
def login():
    pass

@app.get('/reviews', response_model=UserReviewResponseModel)
def create_review(review: UserReviewRequestModel):
    return user_review

@app.post('/reviews', response_model=UserReviewResponseModel)
def create_review(review: UserReviewRequestModel):
    
    user_review = UserReview.create(
        user_id=review.user_id,
        movie_id=review.user_id,
        review=review.review
    )

    return user_review
