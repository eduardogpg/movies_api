from typing import List

from fastapi import Response
from fastapi import APIRouter
from fastapi import HTTPException

from fastapi.security import HTTPBasicCredentials

from ..database import User
from ..database import Movie

from ..schemas import UserRequestModel
from ..schemas import UserResponseModel

from ..schemas import UserReviewResponseModel

router = APIRouter(prefix='/api/v1/users')

@router.post('')
async def root(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(status_code=409, detail='User already exists')

    password = User.create_password(user.password)

    user = User.create(
        username=user.username, 
        password=password
    )

    return user


@router.post('/login', response_model=UserResponseModel)
def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username==credentials.username).first()
    
    if user and user.password == User.create_password(credentials.password):
        response.set_cookie(key='user_id', value=user.id)
        
        return user

    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.get('/reviews/{user_id}', response_model=List[UserReviewResponseModel])
def get_reviews(user_id):
    user = User.select().where(User.id == user_id).first()

    if user:
        return [ review for review in user.reviews.join(Movie)]

    else:
        raise HTTPException(status_code=404, detail="User not found")
