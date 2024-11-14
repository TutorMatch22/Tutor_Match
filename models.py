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
    #email = db.Column(db.String(255), unique=True, nullable=False)#email added 120->200
    password = db.Column(db.String(100), nullable=False)
    photo_path = db.Column(db.String(120), nullable=False)

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    days_available = db.Column(db.String(100), nullable=False)  # days in a week like monday, tuesday, etc.
    time_slots = db.Column(db.String(100), nullable=False)  # times available like 9-10, 14-15, etc.
    reviews = db.Column(db.Integer, nullable=False)  # Number of reviews
    review_text = db.Column(db.Text, nullable=True)  # Actual review text (single review)
    image_path = db.Column(db.String(255), nullable=True)  # Path to the tutor's image

    def __repr__(self):
        return f'Tutor({self.name}, {self.subject}, {self.rating}, {self.reviews} reviews, Review: {self.reviews}, Image Path: {self.image_path})'
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    booked_date = db.Column(db.Date, nullable=False)
    booked_time = db.Column(db.String(20), nullable=False)  # Store the booked time slot
    user = db.relationship('User', backref='bookings')
    tutor = db.relationship('Tutor', backref='bookings')

    def __repr__(self):
        return f'Booking({self.user.username} with {self.tutor.name} on {self.booked_date})'
