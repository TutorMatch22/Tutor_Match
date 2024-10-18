# main.py
from flask import Flask, render_template, request, redirect, url_for, flash
from forms import LoginForm, RegistrationForm  # Import forms from forms.py
from models import db, User, Tutor  # Import models from models.py
from flask_mail import Mail, Message
import random # for generating random tutor data
from faker import Faker # libraries for random tutor names
import random
from models import Tutor
from datetime import datetime
fake = Faker()
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x07\x8a\x9b\xe2\xb2*\x1f\xbd>\xe8\x8aT\xa0\xec\xb9V%i7v\xb0h\x9f\x14'
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "tutors.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#**for email**
#app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # **Example using Gmail**
#app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = 'studyconnect7@gmail.com'  # **Add your email**
#app.config['MAIL_PASSWORD'] = 'TutorMatch$1234'  # **Add your email password**

#mail = Mail(app)
# initialize the database with the Flask app
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            flash(f'Logged in successfully as {form.username.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # don't need constructor in User() since sqlalchemy has deafult one
        new_user = User(username=form.username.data, password=form.password.data)#email=form.email.data
        db.session.add(new_user)
        db.session.commit()
        #email message start
        #msg = Message('Welcome to Tutor Match!', recipients=[form.email.data])
        #msg.body = f'Hello {form.username.data},\n\nThank you for registering with Tutor Match!'
        #mail.send(msg)
        #email message end
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

def generate_random_time_slots():
    # generate random time slots
    slots = []
    for _ in range(random.randint(1, 5)):  # 1-5 time slots
        start_hour = random.randint(7, 22)  # hour between 7:00 and 22:00
        start_minute = random.choice(['00', '30'])  # either 00 or 30 m start
        end_hour = start_hour + 1  # 1 hour long slot
        slots.append(f'{start_hour:02}:{start_minute}-{end_hour:02}:{start_minute}')
    return ', '.join(slots)

@app.route('/tutors')
def tutors():
    # fetch all tutors from the database (query)
    all_tutors = Tutor.query.all()
    return render_template('tutors.html', tutors=all_tutors)

# rm instance/tutors.db to reset the database
def add_dummy_data():
    # if there are no tutors in the database -> add dummy data
    if Tutor.query.count() == 0:
        dummy_tutors = []
        for _ in range(150):  
            name = fake.name()  # random name
            subject = random.choice(['Math', 'Physics', 'Chemistry', 'Biology', 'History', 'English'])
            rating = round(random.uniform(1.0, 5.0), 1)  # random rating between 1.0 and 5.0 rounded to 1 decimal place
            reviews = random.randint(1, 500)  # random number of reviews from 1 to 500
            days_available = random.sample(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], random.randint(1, 7))  # 1-7 days available
            time_slots = generate_random_time_slots()

            dummy_tutor = Tutor(
                name=name,
                subject=subject,
                rating=rating,
                days_available=', '.join(days_available),  # convert list to a comma-separated string
                time_slots=time_slots,
                reviews=reviews  # random number of reviews from 1-500
            )
            dummy_tutors.append(dummy_tutor)

        db.session.bulk_save_objects(dummy_tutors)
        db.session.commit()
        print("150 Tutor data has been added!")

@app.route('/find_tutors', methods=['GET'])
def filter_tutors_subject():
    subject = request.args.get('subject')
    min_rating = request.args.get('rating', type=float)  # Get the rating and convert to float
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Initialize the query
    query = Tutor.query

    # Apply subject filter if provided
    if subject:
        query = query.filter_by(subject=subject)

    # Apply rating filter if provided
    if min_rating is not None:
        query = query.filter(Tutor.rating >= min_rating)

    # Apply time filter if both start_time and end_time are provided
    if start_time and end_time:
        start_time_dt = datetime.strptime(start_time, '%H:%M')
        end_time_dt = datetime.strptime(end_time, '%H:%M')

        all_tutors = query.all()
        filtered_tutors = []

        for tutor in all_tutors:
            # Iterate through each tutor's time slots and check if they overlap
            for slot in tutor.time_slots.split(', '):
                slot_start_str, slot_end_str = slot.split('-')
                slot_start = datetime.strptime(slot_start_str, '%H:%M')
                slot_end = datetime.strptime(slot_end_str, '%H:%M')

                # Check if tutor's slot overlaps with user's requested time
                if (slot_start <= start_time_dt < slot_end) or (slot_start < end_time_dt <= slot_end):
                    filtered_tutors.append(tutor)
                    break  # No need to check other slots for this tutor once a match is found

        # If no tutors match the time filter, return an empty list
        filtered_tutors = filtered_tutors if filtered_tutors else []
    else:
        # If no time filter provided, get all tutors from the query
        filtered_tutors = query.all()

    return render_template('find_tutors.html', tutors=filtered_tutors)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create all tables in the database
        add_dummy_data()  # if the Tutor table is empty add dummy data

    app.run(debug=True)
