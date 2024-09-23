
import pytest
from main import app  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
# resolve errors here by adding html later
def test_home_page(client):
    """Test if the home page renders correctly."""
    response = client.get('/')
    assert response.status_code == 200 # means the page is loading correctly (http)
    assert b"Welcome" in response.data 
# just setting up configuration management
def test_tutors_page(client):
    """Test if the tutors page renders correctly."""
    response = client.get('/tutors')
    assert response.status_code == 200
    assert b"Tutor testing" in response.data  
