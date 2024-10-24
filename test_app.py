import pytest
from main import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()  
            db.create_all()  
        yield client
        with app.app_context():
            db.drop_all()


def test_homepage(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Find Your Ideal Tutor" in rv.data


def test_login_page(client):
    rv = client.get('/login')
    assert rv.status_code == 200
    assert b"Login" in rv.data

def test_register_page(client):
    rv = client.get('/register')
    assert rv.status_code == 200
    assert b"Register" in rv.data


def test_unsuccessful_registration(client):
    rv = client.post('/register', data={
        'username': 'testuser',
        'password': 'Test@1234',
        'confirm_password': 'WrongPass'
    })
    assert rv.status_code == 200  # should not redirect for invalid form
    assert b'Passwords must match' in rv.data  

def test_successful_registration(client):
    rv = client.post('/register', data={
        'username': 'validuser',
        'password': 'Valid@1234',
        'confirm_password': 'Valid@1234'
    }, follow_redirects=True)  

    assert rv.status_code == 200 

def test_successful_login(client):
    client.post('/register', data={
        'username': 'uniqueuser',
        'password': 'Valid@1234',
        'confirm_password': 'Valid@1234'
    }, follow_redirects=True)
    
    rv = client.post('/login', data={
        'username': 'uniqueuser',
        'password': 'Valid@1234'
    }, follow_redirects=True)

    assert rv.status_code == 200
    assert b"Logged in successfully" in rv.data

def test_unsuccessful_login(client):
    rv = client.post('/login', data={
        'username': 'wronguser',
        'password': 'wrongpass'
    })
    assert rv.status_code == 200 # should not redirect for invalid form
   
