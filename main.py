# main.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from forms import LoginForm, RegistrationForm  # Import forms from forms.py
from models import db, User, Tutor  # Import models from models.py
from flask_mail import Mail, Message
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_login import current_user, LoginManager
from werkzeug.utils import secure_filename
import random # for generating random tutor data
from faker import Faker # libraries for random tutor names
from datetime import datetime
from functools import wraps
import os
fake = Faker()
app = Flask(__name__, static_folder='static', template_folder=os.path.join(os.getcwd(), 'templates'))

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = '\x07\x8a\x9b\xe2\xb2*\x1f\xbd>\xe8\x8aT\xa0\xec\xb9V%i7v\xb0h\x9f\x14'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/users-profiles')
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
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next_page = request.args.get('next')  
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['user_id'] = user.id
            print(user.photo_path)
            flash(f'Logged in successfully as {form.username.data}!', 'success')
            # added next tp redirect to the page the user was trying to access before logging in
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('logIn.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # we want to remove user ID from the session
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home'))

# basically how log in and log out works is that when a user logs in, their user ID is stored in the session so that the server knows that the user is logged in. When the user logs out, the user ID is removed from the session.
# function to check if user is logged in

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in to access this page.', 'danger')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
os.makedirs(app.config['UPLOADED_PHOTOS_DEST'], exist_ok=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): 
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash(f'Username "{form.username.data}" is already taken. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)

        photo = form.photo.data
        filename = secure_filename(photo.filename)
        username = form.username.data
        photo_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], username + filename)
        photo.save(photo_path)  # Save to server
        
        # Store relative path or filename in the database
        new_user = User(
            username=form.username.data,
            password=form.password.data,
            photo_path=f"users-profiles/{username + filename}"
        )
        
        db.session.add(new_user)
        db.session.commit()

        #email message start
        #msg = Message('Welcome to Tutor Match!', recipients=[form.email.data])
        #msg.body = f'Hello {form.username.data},\n\nThank you for registering with Tutor Match!'
        #mail.send(msg)
        #email message end
    
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    else:
        for errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'danger')
    
    # Render the profile page with the user data and image path
    return render_template('register.html', form=form)

def generate_random_time_slots():
    slots = []
    taken_slots = []

    for _ in range(random.randint(1, 7)):  # 1-7 time slots per day available
        while True:
            start_hour = random.randint(7, 21)  # between 7 AM and 9 PM start time
            start_minute = random.choice([0, 30])  # minute either 00 or 30
            end_hour = start_hour + 1  # 1-hour lessons
            potential_slot = (start_hour, start_minute, end_hour)
            overlap = False

            for taken_start_hour, taken_start_minute, taken_end_hour in taken_slots:
                taken_start_total_minutes = taken_start_hour * 60 + taken_start_minute
                taken_end_total_minutes = taken_end_hour * 60 + taken_start_minute  

                potential_start_total_minutes = start_hour * 60 + start_minute
                potential_end_total_minutes = end_hour * 60 + start_minute

                if not (potential_end_total_minutes <= taken_start_total_minutes or
                        potential_start_total_minutes >= taken_end_total_minutes):
                    overlap = True
                    break

            if not overlap:
                slots.append(f'{start_hour:02}:{start_minute:02}-{end_hour:02}:{start_minute:02}')
                taken_slots.append(potential_slot)
                break  

    return ', '.join(slots)

image_folder = 'static/tutors-profiles' # folder containing tutor profile images

# all image files in the directory
def get_image_list(folder):
    return [f for f in os.listdir(folder) if f.endswith('.png')] 

# limit text display for reviews
def truncate_text(text, max_length=100):
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text

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
        images = get_image_list(image_folder)  # Load image list for dummy data
        review_templates = [
            "{name} worked with both my kids and was extremely helpful and supportive. They're also prompt with responses and always follows up, which is not my experience with some others we've worked with. So glad to have found them!",
            "While my son was struggling with {subject}, I could not help him. {name} stood out on TutorMatch and we booked him. My son is now getting a good foundation in {subject} and succeeding. Give {name} a chance. Well worth the money.",
            "{name} is tutoring my daughter for the {subject} exam - and we all feel so lucky to have found them. We couldn't ask for a better teacher. Smart, kind and patient - with excellent teaching methods, {name} is an exceptional tutor!",
            "{name} was willing to meet last minute with my daughter to prepare her for a quiz. They were able to quickly assess what the problem was and explain how to do the problem in a way that my daughter understood. {name} is wonderful and we look forward to continuing sessions with them.",
            "{name} did a great job helping my daughter who was struggling in {subject}. {name} is great at assessing the student's individual strengths and weaknesses and providing extra explanations and practice in the areas they struggle. My daughter really enjoyed working with him, and her grades really improved.",
            "{name} is our number one tutor, the kind of tutor that every student needs and wishes they had. They tutored me in a complex and difficult course in {subject} and presented the material so that it clear, simple ans easy to understand.",
            "My daughter has been working with {name} for over a year now and it has changed our lives! My daughter has a very busy schedule so homework time has always been extremely stressful! {name} has been a great asset! They're incredibly flexible and accommodating with her schedule.",
            "I had my first session with {name} and we jumped right into the thick of it wasting no time. Time is money so I appreciated it a lot. {name} is knowledgeable and talked to me in a way I can understand. Amazing tutor for my {subject}. I've already set up multiple sessions!",
            "If I could give 10 out of 5 stars, I would! {name} has been helping my daughter for eight months navigate {subject} - and has done an amazing job at teaching her basic concepts, rebuilding missed concepts from her prior classes, identifying learning gaps and filling them in.",
            "{name} is genuinely one of the best tutors I've had the pleasure of working with. They've been able to help me work through and debug code for some tricky {subject} assignments. Their explanations are thorough, and they always comes to the sessions prepared. :)",
        ]

        for _ in range(150):  
            name = fake.name()  # random name
            subject = random.choice(['Math', 'Physics', 'Chemistry', 'Biology', 'History', 'English'])
            rating = round(random.uniform(1.0, 5.0), 1)  # random rating between 1.0 and 5.0 rounded to 1 decimal place
            reviews = random.randint(1, 200)  # random number of reviews from 1 to 200
            review_text = random.choice(review_templates).format(name=name, subject=subject) # generate reviews from template
            # review_text = truncate_text(review_text, max_length=300) # limit text
            days_available = random.sample(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], random.randint(1, 7))  # 1-7 days available
            time_slots = generate_random_time_slots()

            pro = random.choice(images)  # Randomly select an image from the loaded list
            image_path = f'{image_folder}/{pro}'

            dummy_tutor = Tutor(
                name=name,
                subject=subject,
                rating=rating,
                days_available=', '.join(days_available),  # convert list to a comma-separated string
                time_slots=time_slots,
                reviews=reviews,  # random number of reviews from 1-200
                review_text=review_text,
                image_path=image_path
            )
            dummy_tutors.append(dummy_tutor)

        db.session.bulk_save_objects(dummy_tutors)
        db.session.commit()
        print("150 Tutor data has been added!")

def sort_tutors(query, sort_by):
    if sort_by == "name":
        query = sorted(query, key=lambda tutor: tutor.name)
    elif sort_by == "rating":
        query = sorted(query, key=lambda tutor: tutor.rating, reverse=True)
    elif sort_by == "reviews":
        query = sorted(query, key=lambda tutor: tutor.reviews, reverse=True)

    return query

@app.route('/find_tutors', methods=['GET'])
@login_required
def filter_tutors_subject():
    subject = request.args.get('subject')
    min_rating = request.args.get('rating', type=float)  # Get the rating and convert to float
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    keyword = request.args.get('keyword')
    sort_by = request.args.get('sort_by')

    # Initialize the query
    query = Tutor.query

    # Apply keyword search (for both name and subject)
    if keyword:  # If a keyword is provided, filter by tutor name or subject
        keyword_lower = keyword.lower()
        query = query.filter(
            (Tutor.name.ilike(f"%{keyword_lower}%")) | (Tutor.subject.ilike(f"%{keyword_lower}%"))
        )

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

        query = filtered_tutors
        
    else:
        query = query.all()

    # Apply sorting using the new function
    if sort_by:
        query = sort_tutors(query, sort_by)

    return render_template('find_tutors.html', tutors=query)

@app.route('/book_session/<int:tutor_id>', methods=['GET', 'POST'])
@login_required
def book_session(tutor_id):
    tutor = Tutor.query.get(tutor_id)  # Fetch the tutor using the tutor_id

    if not tutor:
        flash('Tutor not found.', 'danger')
        return redirect(url_for('tutors'))

    if request.method == 'POST':
        bookedDate = request.form['date']
        selected_date = datetime.strptime(bookedDate, '%Y-%m-%d').date()
        current_date = datetime.now().date()

        if selected_date < current_date:
            flash('Please select a date that is today or in the future.', 'danger')
            return redirect(url_for('book_session', tutor_id=tutor_id))

        # TODO: save booking details in the database
        flash(f'Successfully booked a session with {tutor.name} on {bookedDate}!', 'success')
        return redirect(url_for('tutors'))  # Redirect back to the tutors page

    return render_template('book_session.html', tutor=tutor)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create all tables in the database
        add_dummy_data()  # if the Tutor table is empty add dummy data

    app.run(debug=True)