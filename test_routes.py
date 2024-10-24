import pytest
from main import app, db, Tutor

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()  
            db.create_all()  
        yield client
        
        with app.app_context():
            db.drop_all()


def test_tutor_page(client):
    rv = client.get('/tutors')
    assert rv.status_code == 200
    assert b"Our Tutors" in rv.data

def test_filter_tutors_subject(client):
    rv = client.get('/find_tutors?subject=Math')
    assert rv.status_code == 200
    assert b"Math" in rv.data

def test_filter_tutors_rating(client):
    rv = client.get('/find_tutors?subject=Math&rating=4')
    assert rv.status_code == 200
    assert b"Math" in rv.data

def test_tutor_time_filter(client):
    rv = client.get('/find_tutors?subject=Math&start_time=09:00&end_time=11:00')
    assert rv.status_code == 200
    assert b"Math" in rv.data
