import datetime
from peewee import *

# pip install mysqlclient

db = MySQLDatabase('fastproject', user='root', password='',
        host='localhost', port=3306)

class BaseModel(Model):
    created_date = DateTimeField(default=datetime.datetime.now)

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = db
        table_name = 'users'
    
    @classmethod
    def create_password(cls, password):
        return password

class Movie(BaseModel):
    title = TextField()

    class Meta:
        database = db
        table_name = 'movies'

class UserReview(BaseModel):
    user = ForeignKeyField(User, backref='reviews')
    movie = ForeignKeyField(Movie, backref='reviews')
    review = TextField()
    score = IntegerField()

    class Meta:
        database = db
        table_name = 'user_reviews'    

# INSERT INTO movies (title, created_date) VALUES ('Five', NOW());
