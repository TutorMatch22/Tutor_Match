# main.py
from flask import Flask, render_template, request, redirect, url_for, flash
from forms import LoginForm, RegistrationForm  # Import forms from forms.py
from models import db, User, Tutor  # Import models from models.py
from flask_mail import Mail, Message
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
    return render_template('logIn.html', form=form)

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



@app.route('/tutors')
def tutors():
    # fetch all tutors from the database (query)
    all_tutors = Tutor.query.all()
    return render_template('tutors.html', tutors=all_tutors)

def add_dummy_data():
    # if there are no tutors in the database -> add dummy data
    if Tutor.query.count() == 0:
        dummy_tutors = [
            Tutor(name='Joe Cool', subject='Math', rating=4.9),
            Tutor(name='Coco Melon', subject='Physics', rating=4.8),
            Tutor(name='Cookie Dough', subject='Chemistry', rating=4.7),
            Tutor(name='Alice Wonderland', subject='Biology', rating=4.6)
        ]  
        db.session.bulk_save_objects(dummy_tutors)
        db.session.commit()
        print("Dummy tutor data has been added!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create all tables in the database
        add_dummy_data()  # if the Tutor table is empty add dummy data

    app.run(debug=True)
