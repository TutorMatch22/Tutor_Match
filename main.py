from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)
# just testing for configuration management, add more later
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tutors')
def tutors():
    tutors_list = [
        {'name': 'tutor1 lastname', 'subject': 'Math', 'rate': '$20/hr'},
        {'name': 'tutor2', 'subject': 'Science', 'rate': '$25/hr'},
        {'name': 'tutor3', 'subject': 'English', 'rate': '$15/hr'}
    ]
    return render_template('tutors.html', tutors=tutors_list)
