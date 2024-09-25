import pytest
from app import app
from models.user import db, User


@pytest.fixture(scope='module')
def test_client():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
    client = app.test_client()  # Use the Flask app instance

    with app.app_context():
        db.create_all()  # Create the tables in the in-memory database

    yield client  # Provide the test client to the test

    with app.app_context():
        db.session.remove()  # Remove any existing database session
        db.drop_all()  # Drop all tables


def test_create_user(test_client):
    response = test_client.post('/users', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    })
    assert response.status_code == 201
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert data['first_name'] == 'John'
    assert data['last_name'] == 'Doe'
    assert data['email'] == 'john.doe@example.com'


def test_get_users(test_client):
    response = test_client.get('/users?page=1&per_page=10')
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_get_user(test_client):
    response = test_client.post('/users', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    })
    user_id = response.get_json()['id']
    response = test_client.get(f'/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['first_name'] == 'Jane'
    assert data['last_name'] == 'Doe'
    assert data['email'] == 'jane.doe@example.com'


def test_update_user(test_client):
    response = test_client.post('/users', json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com"
    })
    user_id = response.get_json()['id']
    response = test_client.put(f'/users/{user_id}', json={
        "first_name": "Alicia",
        "email": "alicia.smith@example.com"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['first_name'] == 'Alicia'
    assert data['email'] == 'alicia.smith@example.com'


def test_delete_user(test_client):
    response = test_client.post('/users', json={
        "first_name": "Bob",
        "last_name": "Brown",
        "email": "bob.brown@example.com"
    })
    user_id = response.get_json()['id']
    response = test_client.delete(f'/users/{user_id}')
    assert response.status_code == 204
    response = test_client.get(f'/users/{user_id}')
    assert response.status_code == 404
