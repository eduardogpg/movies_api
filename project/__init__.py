from fastapi import Cookie
from fastapi import FastAPI
from fastapi import Response
from fastapi import HTTPException

from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials

from typing import List

from .database import db

from .database import User
from .database import Movie
from .database import UserReview

from .schemas import UserRequestModel
from .schemas import UserResponseModel

from .schemas import UserReviewRequestModel
from .schemas import UserReviewResponseModel
from .schemas import UserReviewUpdateRequestModel

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

    if User.select().where(User.username == user.username).exists():
        return HTTPException(status_code=409, detail='User already exists')

    password = User.create_password(user.password)

    user = User.create(
        username=user.username, 
        password=password
    )

    return user

@app.post('/users/login', response_model=UserResponseModel)
def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username==credentials.username).first()
    
    if user and user.password == User.create_password(credentials.password):
        response.set_cookie(key='user_id', value=user.id)
        
        return user

    else:
        raise HTTPException(status_code=404, detail="User not found")

# TODO -> Listado de todos los usuarios!
@app.post('/reviews', response_model=UserReviewResponseModel)
def create_review(review: UserReviewRequestModel):
    
    user = User.select().where(User.id == review.user_id).first()
    movie = Movie.select().where(Movie.id == review.movie_id).first()

    if user and movie:
    
        user_review = UserReview.create(
            user=user, movie=movie,
            review=review.review,
            score=review.score
        )
        
        return user_review

    else:
        raise HTTPException(status_code=404, detail="User or movie not found")

# @app.get('/reviews/{user_id}', response_model=List[UserReviewResponseModel])
# def get_reviews(user_id):
#     user = User.select().where(User.id == user_id).first()

#     if user:
#         return [ review for review in user.reviews.join(Movie)]

#     else:
#         raise HTTPException(status_code=404, detail="User not found")

@app.get('/reviews/', response_model=List[UserReviewResponseModel])
def update_review(limit: int = 10, page: int = 1):
    return [
        user_review for user_review in UserReview.select().join(Movie).paginate(page, limit)
    ]

@app.put('/reviews/{review_id}', response_model=UserReviewResponseModel)
def update_review(review_id, review: UserReviewUpdateRequestModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review:
        user_review.review = review.review
        user_review.score = review.score
        user_review.save()

        return user_review

    else:
        raise HTTPException(status_code=404, detail="Review not found")

@app.delete('/reviews/{review_id}', response_model=UserReviewResponseModel)
def update_review(review_id):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review:
        user_review.delete_instance()
        return user_review

    else:
        raise HTTPException(status_code=404, detail="Review not found")