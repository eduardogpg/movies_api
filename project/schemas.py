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

""" ------- User ------- """

class UserBaseModel(BaseModel):
    username: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class UserRequestModel(UserBaseModel):
    password: str

class UserResponseModel(UserBaseModel):
    pass

""" ------- Review ------- """

class UserReviewBaseModel(BaseModel):
    user_id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class UserReviewRequestModel(UserReviewBaseModel):
    movie_id: int
    review: str
    score: int

class UserReviewResponseModel(UserReviewBaseModel):
    id: int

# NOW();