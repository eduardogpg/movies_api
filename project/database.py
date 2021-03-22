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

    def __str__(self):
        return self.username

class Movie(BaseModel):
    title = TextField()

    class Meta:
        database = db
        table_name = 'movies'

class UserReview(BaseModel):
    user = ForeignKeyField(User, backref='reviews')
    movie = ForeignKeyField(Movie)
    review = TextField()
    score = IntegerField()

    class Meta:
        database = db
        table_name = 'user_reviews' 

    def __str__(self):
        return self.review   

# INSERT INTO movies (title, created_date) VALUES ('Five', NOW());

user = User.select