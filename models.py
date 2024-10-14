from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# primary_key=True  sets it as the primary key
# makes each id unique and an identifier for each user.
# nullable=False -> field cannot be left empty when creating a new user
# unique=True means that each username must be unique
# db.String(100) makes max length of password/username 100 characters
# models.py


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)#email added 120->200
    password = db.Column(db.String(100), nullable=False)


class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'Tutor({self.name}, {self.subject}, {self.rating})'
