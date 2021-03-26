from typing import Any

from peewee import ModelSelect

from pydantic import BaseModel
from pydantic.utils import GetterDict

class PeeweeGetterDict(GetterDict):    
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        
        return res

class DatabaseBaseModel(BaseModel):

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

""" ------- User ------- """

class UserBaseModel(DatabaseBaseModel):
    username: str

class UserRequestModel(UserBaseModel):
    password: str

class UserResponseModel(UserBaseModel):
    id: int

""" ------- Movie ------- """

class MovieBaseModel(DatabaseBaseModel):
    id: int
    title: str

""" ------- User Review ------- """

class UserReviewBaseModel(DatabaseBaseModel):
    review: str
    score: int

class UserReviewRequestModel(UserReviewBaseModel):
    user_id: int 
    movie_id: int
    
class UserReviewResponseModel(UserReviewBaseModel):
    review: str
    score: int
    movie: MovieBaseModel

class UserReviewUpdateRequestModel(UserReviewBaseModel):
    review: str
    score: int
