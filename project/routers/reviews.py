from typing import List

from fastapi import APIRouter
from fastapi import HTTPException

from ..database import User

from ..schemas import UserRequestModel

from ..schemas import UserReviewRequestModel
from ..schemas import UserReviewResponseModel
from ..schemas import UserReviewUpdateRequestModel

router = APIRouter(prefix='/api/v1/reviews')

@router.post('/reviews', response_model=UserReviewResponseModel)
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


@router.get('/reviews/', response_model=List[UserReviewResponseModel])
def update_review(limit: int = 10, page: int = 1):
    return [
        user_review for user_review in UserReview.select().join(Movie).paginate(page, limit)
    ]

@router.put('/reviews/{review_id}', response_model=UserReviewResponseModel)
def update_review(review_id, review: UserReviewUpdateRequestModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review:
        user_review.review = review.review
        user_review.score = review.score
        user_review.save()

        return user_review

    else:
        raise HTTPException(status_code=404, detail="Review not found")

@router.delete('/reviews/{review_id}', response_model=UserReviewResponseModel)
def update_review(review_id):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review:
        user_review.delete_instance()
        return user_review

    else:
        raise HTTPException(status_code=404, detail="Review not found")