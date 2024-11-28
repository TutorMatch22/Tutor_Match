import os
import pytest
from main import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), 'instance', 'test_tutors.db')}"
    os.makedirs(os.path.join(os.getcwd(), 'instance'), exist_ok=True)

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            test_user = User(username="testuser", password="password", photo_path="test.jpg")
            db.session.add(test_user)
            db.session.commit()

        yield client

        with app.app_context():
            db.drop_all()


def login(client):
    """Simulate user login by setting the session directly."""
    with client.session_transaction() as session:
        session['user_id'] = 1  


def test_tutor_page(client):
    rv = client.get('/tutors')
    assert rv.status_code == 200
    assert b"Our Tutors" in rv.data


def test_filter_tutors_subject(client):
    login(client)  
    rv = client.get('/find_tutors?subject=Math')
    assert rv.status_code == 200
    assert b"Math" in rv.data


def test_filter_tutors_rating(client):
    login(client) 
    rv = client.get('/find_tutors?subject=Math&rating=4')
    assert rv.status_code == 200
    assert b"Math" in rv.data


def test_tutor_time_filter(client):
    login(client)  
    rv = client.get('/find_tutors?subject=Math&start_time=09:00&end_time=11:00')
    assert rv.status_code == 200
    assert b"Math" in rv.data
